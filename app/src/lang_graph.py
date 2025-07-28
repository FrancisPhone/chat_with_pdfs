from src.agents.clarification import clarify_query
from src.agents.routing import route_query
from src.agents.retrieval import retrieve_and_answer
from src.agents.web_search import web_search
from src.agents.answer import generate_answer
from langgraph.graph import StateGraph, END
from src.data_models import State

from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from src.memory import MemoryManager
from src.config import TAVILY_API_KEY


llm = ChatOpenAI(model="gpt-4o-mini")
tavily = TavilyClient(api_key=TAVILY_API_KEY)
memory = MemoryManager()


def clarification_node(state: State) -> State:
    state["clarified_query"] = clarify_query(state["query"], state["session_id"], llm, memory)
    return state


def routing_node(state: State) -> State:
    if state["web_search"]:
        state["route_decision"] = 'web'
    else:
        state["route_decision"] = route_query(state["clarified_query"], llm)
    return state


def retrieval_node(state: State) -> State:
    if state["route_decision"] == "pdf":
        state["context"] = retrieve_and_answer(state["clarified_query"], llm)
    else:
        state["context"] = web_search(state["clarified_query"], llm, tavily)
    return state


def answer_node(state: State) -> State:
    state["response"] = generate_answer(state["clarified_query"], state["context"], state["session_id"], llm, memory)
    return state


workflow = StateGraph(State)
workflow.add_node("clarify", clarification_node)
workflow.add_node("route", routing_node)
workflow.add_node("retrieve", retrieval_node)
workflow.add_node("answer", answer_node)
workflow.add_edge("clarify", "route")
workflow.add_edge("route", "retrieve")
workflow.add_edge("retrieve", "answer")
workflow.add_edge("answer", END)
workflow.set_entry_point("clarify")
graph = workflow.compile()