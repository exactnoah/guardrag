"""LLM client abstraction."""


class LLMClient:
    """Interface for LLM interactions."""
    
    def __init__(self, model_name: str, api_key: str = None):
        """Initialize LLM client.
        
        Args:
            model_name: Name of the LLM model
            api_key: API key for the model (optional)
        """
        self.model_name = model_name
        self.api_key = api_key
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text
        """
        pass
    
    def stream_generate(self, prompt: str, **kwargs):
        """Stream text generation.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional generation parameters
            
        Yields:
            Text chunks
        """
        pass
