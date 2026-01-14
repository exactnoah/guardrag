"""Retrieval recall metric implementation."""


def compute_recall(retrieved_docs: list[str], relevant_docs: list[str]) -> float:
    """Compute recall for retrieval.
    
    Measures what fraction of relevant documents were retrieved.
    
    Args:
        retrieved_docs: Documents returned by retriever
        relevant_docs: Known relevant documents
        
    Returns:
        Recall score (0-1)
    """
    pass
