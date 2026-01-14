"""FastAPI application setup."""

from fastapi import FastAPI

app = FastAPI(
    title="GuardRAG",
    description="Local RAG evaluation system API",
    version="0.1.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
