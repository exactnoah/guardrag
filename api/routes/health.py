"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """Check API health status.
    
    Returns:
        Health status
    """
    return {"status": "healthy"}
