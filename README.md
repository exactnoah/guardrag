# GuardRag — Project Explanation

## Project Overview
**GuardRag** is a locally run Retrieval-Augmented Generation (RAG) system designed to answer questions over a private document corpus. The system:

- Ingests documents
- Indexes them using embeddings
- Retrieves relevant content for a query
- Uses a local language model to generate answers grounded in retrieved sources

In addition to basic RAG functionality, the project includes an **evaluation and CI pipeline** that automatically benchmarks model responses against prior outputs. This helps detect context loss, track regression, and reduce ungrounded or misleading responses.

---

## What the System Does (End-to-End)

### 1. Knowledge Ingestion
The system ingests documents from local sources, including:

- PDFs
- Markdown files
- Source code
- Internal documentation

During ingestion, documents are:

- Split into semantic chunks
- Tagged with metadata:
  - Source
  - Date
  - Document type
  - Topic
- Converted into vector embeddings
- Stored locally with associated metadata

**Notes:**
- Ingestion runs fully offline
- No external APIs are used

---

### 2. Indexing and Retrieval
- Embeddings are stored in a vector index (**FAISS**)
- Metadata is stored separately (**SQLite** or **DuckDB**)

When a user submits a query:

- The query is embedded
- A vector search retrieves the top-*k* most relevant chunks
- Optional metadata filters are applied:
  - Date
  - Source
  - Document type
- Only selected chunks are passed to the language model

This design avoids sending full documents or large context windows to the model.

---

### 3. Answer Generation
- A local language model (via **Ollama**) generates responses

Generation behavior:

- Uses **only** retrieved chunks as context
- Produces a direct answer to the query
- Includes references to source chunks
- Refuses to answer if no supporting context is retrieved

---

### 4. Evaluation and Continuous Integration
The project includes a predefined evaluation dataset containing:

- Questions
- Expected answer properties
- Required or acceptable source documents

Automated evaluation measures:

- Retrieval recall
- Answer faithfulness to sources
- Latency
- Hallucination rate

**CI Integration:**

- Evaluations run in **GitHub Actions**
- Performance thresholds are enforced
- CI fails if regressions are detected

---

## Core Capabilities
The system:

- Ingests and indexes structured and unstructured documents locally
- Performs semantic search with metadata constraints
- Generates evidence-grounded responses using a local LLM
- Provides source attribution for all answers
- Automatically evaluates system behavior via CI
- Runs fully offline with optional containerization

---

## Technology Stack (Summary)

- **LLM:** Ollama (LLaMA 3.1 8B or similar)
- **Embeddings:** SentenceTransformers
- **Vector Search:** FAISS
- **Backend API:** FastAPI (Python)
- **Evaluation:** Custom metrics, MLflow (optional)
- **CI:** GitHub Actions
- **Storage:** SQLite or DuckDB
- **Containerization:** Docker (optional)

---

## Repository Structure (Purpose-Focused)

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

---

## Scope Notes
- Focuses on backend systems rather than frontend UI
- Autonomous actions (if implemented) are:
  - Constrained
  - Auditable
  - Optional
- Evaluation and CI are core components, not add-ons
- Cloud services are not required for normal operation

---

## Summary
GuardRag is a local RAG system that combines document ingestion, semantic retrieval, and LLM-based generation with automated evaluation and CI. The project prioritizes predictable behavior, source-grounded outputs, and repeatable testing over scale or raw model capability.
