from tavily import TavilyClient
from langchain_openai import ChatOpenAI


def web_search(query: str, llm: ChatOpenAI, tavily: TavilyClient) -> str:
    results = tavily.search(query=query, max_results=3)
    context = "\n".join([result["content"] for result in results["results"]])
    prompt = f"Based on the web search results: {context}\nAnswer the query: {query}"
    response = llm.invoke(prompt)
    return response.content