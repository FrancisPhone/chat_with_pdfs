from langchain_openai import ChatOpenAI
from src.memory import MemoryManager


def generate_answer(query: str, context: str, session_id: str, llm: ChatOpenAI, memory: MemoryManager) -> str:
    history = memory.get_session_history(session_id)
    prompt = f"""
    Conversation history: {history}
    Context: {context}
    Query: {query}
    Provide a concise and accurate answer.
    """
    response = llm.invoke(prompt)
    memory.add_message(session_id, {"query": query, "answer": response.content})
    return response.content