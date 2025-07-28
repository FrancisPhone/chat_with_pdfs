from typing import Dict, Any
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    session_id: str
    web_search: bool = False


class State(Dict[str, Any]):
    query: str
    session_id: str
    clarified_query: str
    route_decision: str
    context: str
    response: str
    web_search: bool