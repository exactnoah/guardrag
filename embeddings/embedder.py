"""Embedding model wrapper."""


class Embedder:
    """Text embedding interface."""
    
    def __init__(self, model_name: str):
        """Initialize embedder.
        
        Args:
            model_name: Name of the embedding model
        """
        self.model_name = model_name
    
    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        pass
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        pass
