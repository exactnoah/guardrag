# GuardRag Sprint Plan

## Sprint 1 (Jan 13 - Jan 26)
**Foundation & Architecture**

- Architecture barebones and repository structure
- Problem definition, scope document, threat model
- Log ingestion pipeline (local files, Docker, GitHub Actions)
- ~~Normalized log schema and sample datasets~~
- Research: Base model selection, tech stack, RAG frameworks, UI options, CI/CD

## Sprint 2 (Jan 27 - Feb 9)
**Data Processing & Embeddings**

- RAG LLM Proof-of-Concept (Investigate using Haystack)
   - See how the Haystack Stack is using semantic chunking and what they're doing for a similarity search api
   - Investigate FAISS vector index and SQLite metadata store
   - Local embeddings with sentence-transformers
- Refine CICD Approach (Sprint 3) and Deep Eval Approach (Sprint 4)
- Removed: ~~Metadata tagging (service, severity, host)~~

## Sprint 3 (Feb 10 - Feb 23)
**RAG Pipeline & LLM Integration**

- Lift and shift logic from PoC to GuardRag Repository
- Investigate UI and try to create minimal PoC (dependencies)
- Continue automation efforts
- Investigative work surrounding context selection and what that entails (benchmarking + severity weighted context selection)
- Investigative work surrounding RAG pipeline, overall design, and sliding window retrieval

- ~~RAG pipeline with sliding window retrieval~~
- ~~Severity-weighted context selection~~
- ~~Ollama integration (LLaMA 3.1 8B primary)~~
- ~~Model benchmarks (Mistral 7B, Phi-3)~~

## Sprint 4 (Feb 24 - Mar 9)
**Classification & Safe Action Planning**

- Log classification engine (known issue, anomaly, noise)
- Root cause analysis with confidence scoring
- Action plan generator (read-only mode)
- Safety constraints and explainability
- YAML action manifests
- UI design discussion
- Prompt templates and model abstraction layer

## Sprint 5 (Mar 10 - Mar 23)
**Controlled Execution & CI Integration**

- Action executor with rollback (restart container, clear cache, rollback config, open issue)
- Sandbox execution and audit logging
- GitHub Actions CI integration
- Failed build diagnosis and PR comment bot

## Sprint 6 (Mar 24 - Apr 6)
**Evaluation & User Interface**

- Evaluation metrics (noise reduction, MTTR, accuracy, false positives)
- Metrics dashboard and automated threshold checks
- CLI/UI with timeline view and decision tracing
- Demo script and documentation

## Sprint 7 (Apr 7 - Apr 20)
**Hardening & Final Delivery**

- Stress testing (log floods, corrupted logs, hallucinations, unsafe actions)
- Edge case handling and known limitations
- Security review
- Final integration testing and documentation
- Capstone presentation materials
