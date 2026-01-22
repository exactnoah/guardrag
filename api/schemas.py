"""Pydantic schemas for API requests/responses."""

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Query request schema."""
    query: str
    top_k: int = 10


class QueryResponse(BaseModel):
    """Query response schema."""
    query: str
    answers: list[str]
    sources: list[str]
