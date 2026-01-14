"""Query endpoint for RAG system."""

from fastapi import APIRouter

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/")
async def query(query: str, top_k: int = 10):
    """Execute a RAG query.
    
    Args:
        query: User query
        top_k: Number of results
        
    Returns:
        Query results
    """
    pass
