from fastapi import FastAPI
from src.data_models import QueryRequest
from scripts.ingest_pdfs import ingest_pdfs
from src.lang_graph import memory, graph
from src.config import VECTOR_STORE_PATH
import os

app = FastAPI()


@app.post("/ask")
async def ask_question(request: QueryRequest):
    state = graph.invoke({"query": request.query, "session_id": request.session_id, "web_search": request.web_search})
    return {"answer": state["response"]}


@app.post("/clear_memory")
async def clear_memory(session_id: str):
    memory.clear_session(session_id)
    return {"message": f"Memory cleared for session {session_id}"}

