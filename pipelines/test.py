"""
Simple RAG Pipeline using Haystack + Ollama
Requires: Ollama running locally with mistral model pulled
"""

import os
import importlib
from pathlib import Path
import shutil



#tkinter gui
from gui import GUI

gui = None

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
OLLAMA_MODEL = "mistral:7b" 
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 4  # Number of documents to retrieve

NEW_DOC = False
indexed_files = set()
RUNNING = True
rag_pipeline = None
indexing_pipeline = None

#GUI functions
def get_file(filepath):
    global NEW_DOC

    #filepath = filedialog.askopenfilename()
    if not filepath:
        return
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    filename = os.path.basename(filepath)
    shutil.copy(filepath, DOCS_DIR / filename)
    print('Selected: ', filename)
    print_on_gui(f"{filename} added to Docs Folder. Click submit to index and add to pipeline." )

    NEW_DOC = True

def print_on_gui(*args, sep=" ", end="\n"):
    text = sep.join(map(str, args)) + end
    print(text)

    if gui:
        gui.print(text)

def handle_submit(question, run_eval, show_sources):
    print("submitted")
    gui.update_bar(10)
    gui.root.after(2000, gui.mainFrame.destroy)


def rag_load():
    print_on_gui("Ready!")
    gui.progressive_bar()
    
def main():
    global gui
    gui = GUI(on_submit=handle_submit, on_upload=get_file)
    print_on_gui("Loading... \n\n")

    gui.root.after(4000, rag_load)
    gui.run()

if __name__ == "__main__":
    main()