# GuardRag — Project Explanation

## Project Overview
**GuardRag** is a locally run Retrieval-Augmented Generation (RAG) system designed to answer questions over a private document corpus. The system also includes an evaluation and CI pipeline that automatically benchmarks model responses against prior outputs. 

The system:

- Ingests and indexes structured and unstructured documents locally
- Performs semantic search with metadata constraints
- Generates evidence-grounded responses using a local LLM
- Provides source attribution for all answers
- Automatically evaluates system behavior via CI
- Runs fully offline with optional containerization

Technology Stack (Summary):

- Python Version: 3.14
- LLM: Ollama (pull Mistral 7B)
- RAG: Haystack
- Backend API: FastAPI (Python)
- Evaluation: Custom metrics, MLflow (optional)
- CI: GitHub Actions
- Storage: SQLite or DuckDB
- Containerization: Docker (optional)


---

# Instructions
### Prerequisites:

Python 3.14 installed

## Setup (One-time)

Run the setup script:

powershell   
```.\setup.ps1```

Ihis will download Ollama if it isn't already on your computer and pull Mistral 7B. Then it will create a virtual environment and install all dependencies (~5-10 minutes)

## Usage

Add your documents to the docs/ folder. 

Currently supports .pdf and .txt files

## Run the pipeline:

powershell   
```python .\pipelines\rag_pipeline.py```

Enter "quit" to exit.


---

## Repository Structure

- `data/` — raw inputs, processed chunks, evaluation datasets  
- `ingestion/` — document loading, chunking, preprocessing  
- `embeddings/` — embedding generation and index management  
- `retrieval/` — vector search, ranking, metadata filtering  
- `generation/` — prompt templates and LLM interaction  
- `evaluation/` — metrics, datasets, evaluators, reports  
- `api/` — query and health endpoints  
- `pipelines/` — indexing and evaluation automation  
- `ci/`, `.github/` — CI logic and workflows  
- `docs/` — architecture, evaluation methodology, design decisions  

### VM
Email Michael Craig (michaelcraig@weber.edu) with requests and cc Brad Peterson as well. Make sure to explain it's for 4760 for the semester.

