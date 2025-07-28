from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from src.config import VECTOR_STORE_PATH


def retrieve_and_answer(query: str, llm: ChatOpenAI) -> str:
    vector_store = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=OpenAIEmbeddings())
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(query)

    prompt = PromptTemplate(
        input_variables=["query", "context"],
        template="Based on the context: {context}\nAnswer the query: {query}"
    )
    context = "\n".join([doc.page_content for doc in docs])
    response = llm.invoke(prompt.format(query=query, context=context))
    return response.content