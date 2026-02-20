# System Architecture

## Overview

GuardRAG follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│           API Layer (FastAPI)           │
├─────────────────────────────────────────┤
│     Pipelines & Orchestration Layer     │
├──────────────┬──────────────┬───────────┤
│  Ingestion   │  Retrieval   │ Generation│
├──────────────┼──────────────┼───────────┤
│  Embeddings  │  Evaluation  │   Index   │
├─────────────────────────────────────────┤
│           Data & Storage Layer          │
└─────────────────────────────────────────┘
```

## Components

### Data Layer (`data/`)
- **raw/**: Original source documents (PDFs, Markdown, code)
- **processed/**: Cleaned, chunked documents ready for embedding
- **evaluation/**: Golden datasets for testing
- **schemas/**: Data validation schemas

### Ingestion (`ingestion/`)
Responsible for loading, chunking, and preprocessing documents.

**Key modules:**
- `loaders/`: PDF, Markdown, code file loaders
- `chunking.py`: Overlapping chunk generation
- `preprocessing.py`: Text cleaning and normalization
- `ingest.py`: Main ingestion pipeline

### Embeddings (`embeddings/`)
Manages text vectorization and vector storage.

**Key modules:**
- `embedder.py`: Text-to-vector conversion
- `index.py`: Vector index for similarity search
- `store.py`: Persistence layer for embeddings

### Retrieval (`retrieval/`)
Implements document retrieval and ranking strategies.

**Key modules:**
- `search.py`: Semantic similarity search
- `ranking.py`: Reranking and relevance scoring
- `filters.py`: Metadata-based filtering

### Generation (`generation/`)
Handles LLM interactions and answer generation.

**Key modules:**
- `llm_client.py`: LLM API abstraction
- `generate.py`: Answer generation pipeline
- `prompts/`: Prompt templates (versioned)

### Evaluation (`evaluation/`)
Core evaluation engine with multiple metrics.

**Key modules:**
- `evaluator.py`: Main evaluation coordinator
- `metrics/`:
  - `faithfulness.py`: Answer-to-context faithfulness
  - `retrieval_recall.py`: Retrieval effectiveness
  - `latency.py`: Performance timing
- `reports.py`: Evaluation reporting

### API (`api/`)
RESTful interface to the RAG system.

**Key modules:**
- `main.py`: FastAPI application setup
- `routes/`: Endpoint implementations
- `schemas.py`: Request/response validation

### Pipelines (`pipelines/`)
Orchestrates multi-step workflows.

**Key modules:**
- `build_index.py`: Index construction from source data
- `run_evaluation.py`: End-to-end evaluation
- `retrain_embeddings.py`: Model updates

## Data Flow

### Ingestion Flow
```
Raw Documents
    ↓
[Load] → [Chunk] → [Preprocess]
    ↓
Processed Chunks
```

### Retrieval Flow
```
User Query
    ↓
[Embed Query] → [Search Index] → [Rerank] → [Filter]
    ↓
Retrieved Documents
```

### Generation Flow
```
Query + Retrieved Docs
    ↓
[Format Prompt] → [Call LLM] → [Parse Response]
    ↓
Generated Answer
```

### Evaluation Flow
```
Predictions + Golden Dataset
    ↓
[Compute Metrics] → [Compare Thresholds] → [Generate Report]
    ↓
Pass/Fail + Metric Scores
```

## Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Testability**: Clear interfaces enable unit and integration testing
3. **Extensibility**: Easy to swap implementations (e.g., different LLMs)
4. **Observability**: Metrics and logging at each layer
5. **Production-Ready**: Proper error handling and configuration management
