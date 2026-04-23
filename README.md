# GuardRag

## Project Overview
GuardRag is a local Retrieval-Augmented Generation (RAG) application that lets users upload private files and ask questions grounded in those files. Check out our [home page](https://exactnoah.github.io/guardrag/)

The system:
- Ingests and indexes `.pdf`, `.docx`, `.txt`, `.csv` and `.json`  documents locally.
- Performs semantic retrieval with Haystack.
- Generates responses through local Ollama models.
- Shows source-backed answers in a simple desktop GUI.

Technology summary:
- Python: 3.10+ (3.14+ recommended)
- LLM runtime: Ollama (`mistral:7b` default)
- RAG framework: Haystack
- API framework: FastAPI (scaffolded)
- Optional container path: Docker

## Installation

### Prerequisites
- Python 3.10+

### One-time setup (Windows)
Run:

```powershell
.\setup.ps1
```

`setup.ps1` calls the consolidated installer at `scripts/install.py`, which:
- Creates/reuses `.venv`
- Installs dependencies from `setup_materials/requirements.txt`
- Creates `.env` from `.env.example` (or a fallback)
- Creates standard runtime directories (`docs`, `data`, `logs`, `config`)
- Pulls `mistral:7b` when Ollama is installed and running

Direct usage:

```bash
python scripts/install.py --model mistral:7b
```

## Run GuardRag

Make sure Ollama is running

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the desktop GUI:

```powershell
python .\pipelines\rag_pipeline.py
```

Type `quit` in the prompt box to exit the app.



## Usage
- Click `File` then `Add File` to copy files into the system.
- Ask questions about the uploaded documents.
- The app will re-index newly added files automatically.

## Repository Structure
- `docs/` - user-uploaded source files
- `pipelines/` - RAG pipeline and evaluation runners
- `project_docs/` - architecture and design notes
- `installer/windows/` - Inno Setup wizard and build scripts
- `scripts/` - consolidated install tooling

