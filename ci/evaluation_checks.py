"""CI checks for evaluation metrics."""

import yaml


def load_thresholds(threshold_path: str = "ci/thresholds.yaml") -> dict:
    """Load evaluation thresholds.
    
    Args:
        threshold_path: Path to thresholds file
        
    Returns:
        Dictionary of thresholds
    """
    with open(threshold_path) as f:
        return yaml.safe_load(f)


def check_thresholds(metrics: dict, thresholds: dict) -> bool:
    """Verify metrics meet thresholds.
    
    Args:
        metrics: Computed metrics
        thresholds: Required thresholds
        
    Returns:
        True if all metrics pass
    """
    pass
