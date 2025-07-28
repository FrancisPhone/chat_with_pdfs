from langchain_openai import ChatOpenAI
from src.memory import MemoryManager


def clarify_query(query: str, session_id: str, llm: ChatOpenAI, memory: MemoryManager) -> str:
    history = memory.get_session_history(session_id)
    prompt = f"""
    Conversation history: {history}
    Analyze the query: "{query}"
    If it is vague or underspecified (e.g., missing context or unclear terms), return a clarified version or a question by looking at the conversation history to ask the chatbot.
    If it is clear, return the original query.
    Example: hisory: "OCR-Free Document Understanding Transformer" paper 
             query: "What is the accuracy?"
             clarified_query: "What is the accuracy of the model in the 'OCR-Free Document Understanding Transformer' paper?"
    """
    response = llm.invoke(prompt)
    return response.content