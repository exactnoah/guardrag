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

- ~~RAG pipeline with sliding window retrieval~~
- ~~Severity-weighted context selection~~
- ~~Ollama integration (LLaMA 3.1 8B primary)~~
- ~~Model benchmarks (Mistral 7B, Phi-3)~~

## Sprint 4 (Feb 24 - Mar 9)

- Research and integrate ragas (evaluation benchmarks) PT. 1
- CI/CD research+integration with DeepEval (soft dependency on RAGAS) PT. 1
     - Main PoC with integrated DeepEval framework can be built out with locally run-workflows, but return dummy values until RAGAS is done.
     - Hard dependency on Installation Wizard work
- Installation Wizard complete (Have DeepEval + Ragas Installed?)
- Research into deep thinking?

## Sprint 5 (Mar 10 - Mar 23)
**Controlled Execution & CI Integration**

- Take performance metrics; Research efficient file storage to integrate with LLMs for RAG.
     - Consider Deep-Eval research (launching other models)
        - Prerequisite of CI work done (DeepEval might dictate how CI) is done.
- Discuss testing strategy (release branches w/ stable versions?)

- ~~Action executor with rollback (restart container, clear cache, rollback config, open issue)~~
- ~~Sandbox execution and audit logging~~
- ~~GitHub Actions CI integration~~
- ~~Failed build diagnosis and PR comment bot~~

## Sprint 6 (Mar 24 - Apr 6)
**Evaluation & User Interface**

- Evaluation metrics (noise reduction, MTTR, accuracy, false positives)
- Metrics dashboard and automated threshold checks
- CLI/UI with timeline view and decision tracing
- Demo script and documentation

## Sprint 7 (Apr 7 - Apr 20)
**Hardening & Final Delivery**

- Prompt templates and model abstraction layer
- Stress testing (log floods, corrupted logs, hallucinations, unsafe actions)
- Edge case handling and known limitations
- Security review
- Final integration testing and documentation
- Capstone presentation materials
