"""Semantic search functionality."""


def semantic_search(query: str, index, embedder, top_k: int = 10) -> list[dict]:
    """Search for documents similar to query.
    
    Args:
        query: Search query
        index: Vector index
        embedder: Embedding model
        top_k: Number of results
        
    Returns:
        List of relevant documents
    """
    pass
