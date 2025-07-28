import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from src.config import DATA_DIR, VECTOR_STORE_PATH


def ingest_pdfs():
    documents = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_DIR, filename))
            documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    Chroma.from_documents(splits, embeddings, persist_directory=VECTOR_STORE_PATH)
    print("PDFs ingested successfully.")