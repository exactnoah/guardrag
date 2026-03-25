# GuardRag

## Project Overview
GuardRag is a local Retrieval-Augmented Generation (RAG) application that lets users upload private files and ask questions grounded in those files.

The system:
- Ingests and indexes `.pdf`, `.docx`, and `.txt` documents locally.
- Performs semantic retrieval with Haystack.
- Generates responses through local Ollama models.
- Shows source-backed answers in a simple desktop GUI.

Technology summary:
- Python: 3.10+
- LLM runtime: Ollama (`mistral:7b` default)
- RAG framework: Haystack
- API framework: FastAPI (scaffolded)
- Optional container path: Docker

## Installation

### Prerequisites
- Python 3.10+
- Ollama installed: `https://ollama.com/download`

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

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the desktop GUI:

```powershell
python .\pipelines\rag_pipeline.py
```

Type `quit` in the prompt box to exit the app.

## Build Windows Wizard Installer

The repo now includes an Inno Setup based wizard installer scaffold.

### Prerequisites
- Inno Setup 6 (`ISCC.exe`) installed
- Python 3.10+

### Quick build (after clone)
1. Open PowerShell in the repository root.
2. (Optional) Verify Python:

```powershell
py --version
```

3. If Inno Setup is not installed (`ISCC.exe` missing), install it:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\installer\windows\install_inno_setup.ps1
```

4. Build the installer:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\installer\windows\build_installer.ps1
```

Output:
- `installer/windows/dist/GuardRag-Setup.exe`

Optional smoke test on a clean machine/VM:
- Run `GuardRag-Setup.exe`
- Complete wizard selections
- Confirm post-install log at `logs/installer-post-install.log`

### Installer behavior
- Copies the project into `Program Files\GuardRag`
- Lets user choose whether to pull `mistral:7b` during install
- Lets user choose whether to launch GuardRag after install
- Runs post-install orchestration via `installer/windows/post_install.ps1`
- Writes post-install logs to `logs/installer-post-install.log`

## Usage
- Click `New File` to attach files.
- Ask questions about the uploaded documents.
- The app will re-index newly added files automatically.

## Repository Structure
- `api/` - API scaffolding
- `ci/` - evaluation thresholds/checks
- `data/` - evaluation and runtime data
- `docs/` - user-uploaded source files
- `evaluation/` - evaluator + metrics scaffolding
- `pipelines/` - RAG pipeline and evaluation runners
- `project_docs/` - architecture and design notes
- `installer/windows/` - Inno Setup wizard and build scripts
- `scripts/` - consolidated install tooling
- `setup_materials/` - installer dependency manifests

