from langchain_openai import ChatOpenAI


def route_query(query: str, llm: ChatOpenAI) -> str:
    prompt = f"""
    Determine if the query "{query}" can be answered using academic papers or requires a web search.
    Return "pdf" for queries related to academic papers, or "web" for queries requiring external information.
    Example: "What did OpenAI release this month?" -> "web"
    Example: "Which prompt template gave the highest zero-shot accuracy in Zhang et al.?" -> "pdf"
    """
    response = llm.invoke(prompt)
    return response.content