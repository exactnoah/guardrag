"""Main evaluation engine."""


class Evaluator:
    """Coordinates evaluation across multiple metrics."""
    
    def __init__(self, metrics: list[str] = None):
        """Initialize evaluator.
        
        Args:
            metrics: List of metric names to compute
        """
        self.metrics = metrics or []
    
    def evaluate(self, results: list[dict]) -> dict:
        """Evaluate results across all metrics.
        
        Args:
            results: Query results to evaluate
            
        Returns:
            Dictionary of metric scores
        """
        pass
