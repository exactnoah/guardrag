# GuardRAG: Local RAG Evaluation System

A production-grade RAG (Retrieval-Augmented Generation) system designed for comprehensive evaluation and optimization of retrieval and generation components.

## Features

- **Modular Architecture**: Clean separation between data ingestion, embeddings, retrieval, and generation
- **Comprehensive Evaluation**: Faithfulness, recall, latency, and custom metrics
- **Production Ready**: FastAPI backend with Docker support
- **CI/CD Integration**: Automated evaluation with quality thresholds
- **Configurable Experiments**: Config-driven experimentation framework

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
git clone <repository-url>
cd guardrag
pip install -r requirements.txt
```

### Basic Usage

```python
from ingestion import loaders, chunking
from embeddings import embedder, index
from retrieval import search
from generation import llm_client, generate

# 1. Ingest documents
documents = loaders.load_pdf("data/raw/document.pdf")
chunks = chunking.chunk_text(documents)

# 2. Create embeddings
emb = embedder.Embedder("sentence-transformers/all-MiniLM-L6-v2")
embeddings = emb.embed_batch([c["text"] for c in chunks])

# 3. Build index
idx = index.VectorIndex(dimension=384)
idx.add(embeddings, [c["id"] for c in chunks])

# 4. Retrieve and generate
query = "What is RAG?"
results = search.semantic_search(query, idx, emb)
llm = llm_client.LLMClient("gpt-4")
answer = generate.generate_answer(query, results, llm)
```

## Project Structure

See [architecture.md](docs/architecture.md) for detailed component descriptions.

## Documentation

- [Architecture](docs/architecture.md) - System design and component responsibilities
- [Evaluation](docs/evaluation.md) - Metrics, datasets, and evaluation methodology
- [Design Decisions](docs/design-decisions.md) - Technical rationale and tradeoffs

## API

Start the API server:

```bash
python -m api.main
```

Health check:
```bash
curl http://localhost:8000/health
```

Query endpoint:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?", "top_k": 10}'
```

## Development

### Testing

```bash
pytest tests/ -v
```

### Code Quality

```bash
black .
ruff check .
mypy .
```

### Docker

```bash
docker-compose up
```

## Contributing

Please ensure all code is tested and passes linting checks before submitting PRs.

## License

MIT License - see LICENSE file for details