# Haystack + Ollama and Mistral:7B RAG Pipeline
### Prerequisites:

Python 3.14 installed

## Setup (One-time)

Run the setup script:

powershell   
```.\setup.ps1```

This will create a virtual environment and install all dependencies (~5-10 minutes)

## Usage

Add your documents to the docs/ folder. 

Currently supports .txt files

## Activate the virtual environment (if not already active):

powershell   
```.\venv\Scripts\Activate.ps1```

Note: (venv) should appear in front of file path in terminal.

Use ```deactivate``` to stop virtual environment.

## Run the pipeline:

powershell   
```python rag_pipeline.py```

Enter "quit" to exit.