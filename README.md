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

Ihis will check if Ollama is already on your computer and pull Mistral 7B. Then it will create a virtual environment and install all dependencies (~5-10 minutes)

## Usage

Add your documents to the docs/ folder. 

Currently supports .pdf, .docx, and .txt files

## Run the pipeline:

## Activate the virtual environment (if not already active):

powershell   
```.\venv\Scripts\Activate.ps1```

Note: (venv) should appear in front of file path in terminal.

Use ```deactivate``` to stop virtual environment.

powershell   
```python .\pipelines\rag_pipeline.py```

Enter "quit" to exit.


---

## Repository Structure

- `data/` — raw inputs, processed chunks, evaluation datasets  
- `evaluation/` — metrics, datasets, evaluators, reports  
- `api/` — rag interface
- `pipelines/` — Haystack rag, evaluation
- `ci/`, `.github/` — CI logic and workflows  
- `docs/` — hold user files
- `project_docs/` — project documentation (sprint plan, design-decisions, etc)
- `setup_materials/` — pull mistral script and requirements

### VM
Email Michael Craig (michaelcraig@weber.edu) with requests and cc Brad Peterson as well. Make sure to explain it's for 4760 for the semester.

