"""Vector store persistence."""


class VectorStore:
    """Abstraction for vector storage backends."""
    
    def save(self, path: str) -> None:
        """Save vector store to disk.
        
        Args:
            path: Path to save location
        """
        pass
    
    def load(self, path: str) -> None:
        """Load vector store from disk.
        
        Args:
            path: Path to load from
        """
        pass
