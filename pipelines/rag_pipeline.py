"""
Simple RAG Pipeline using Haystack + Ollama
Requires: Ollama running locally with mistral model pulled
"""

import os
import importlib
from pathlib import Path
import shutil
import hashlib

from evaluation import run_evaluation
from logger import log_entry, start_eval_log

from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.writers import DocumentWriter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack.components.preprocessors import DocumentSplitter
from pypdf import PdfReader



#tkinter gui
from gui import GUI

gui = None

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)
STORE_PATH = CACHE_DIR / "embeddings.json"
HASH_PATH = CACHE_DIR / "docs_hash.txt"
OLLAMA_MODEL = "mistral:7b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 4

NEW_DOC = False
indexed_files = set()
rag_pipeline = None
indexing_pipeline = None


def compute_docs_hash():
    if not DOCS_DIR.exists():
        return ""

    entries = []
    for file in sorted(DOCS_DIR.iterdir()):
        if file.is_file():
            stat = file.stat()
            entries.append(f"{file.name}:{stat.st_mtime}:{stat.st_size}")

    joined = "|".join(entries)
    return hashlib.md5(joined.encode()).hexdigest()


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
    print_on_gui(f"{filename} added to Docs Folder. Click submit to index and add to pipeline.")

    NEW_DOC = True

def print_on_gui(*args, sep=" ", end="\n"):
    text = sep.join(map(str, args)) + end
    print(text)

    if gui:
        gui.print(text)

def handle_submit(question, run_eval, show_sources):
    global rag_pipeline, NEW_DOC


    if NEW_DOC and indexing_pipeline is not None:
        print_on_gui("\nNew doc detected, indexing and appending...")
        new_documents = load_documents(DOCS_DIR, only_new=True)

        if new_documents:
                indexing_pipeline.run({"splitter": {"documents": new_documents}})
                indexing_pipeline.get_component("writer").document_store.save_to_disk(STORE_PATH)
                newhash = compute_docs_hash()
                HASH_PATH.write_text(newhash)

                print_on_gui("\nNew Document Added")
        else:
                print_on_gui("No new documents found")
        NEW_DOC = False
    
    if not question or question == "":
        gui.root.after(500, gui.delete_bar)
        gui.submit["state"] = "normal"
        gui.entry["state"] = "normal"
        return
    
    if question.lower() in ['quit', 'exit', 'q']:
        print_on_gui("Goodbye!")
        gui.after(3000, gui.destroy)
        return
    
    print_on_gui("\nThinking...")
    result = rag_pipeline.run({
        "text_embedder": {"text": question},
        "prompt_builder": {"question": question}
    },
        include_outputs_from=["retriever"]
    )

    answer = result["llm"]["replies"][0]
    retrieved_docs = result["retriever"]["documents"]
    sources = [doc.meta.get("filename", "Unknown") for doc in retrieved_docs]


    if run_eval and retrieved_docs:
        #write query and response to eval log
        start_eval_log(question, answer, sources)
        run_evaluation(question, answer, retrieved_docs, print_on_gui)

    print_on_gui(answer)
    #log the query, response, and sources
    log_entry(question, answer, sources)
    gui.load_logs()
        
    if show_sources and retrieved_docs:
        print_on_gui("\n--- Sources ---")
        for i, doc in enumerate(retrieved_docs, 1):
            filename = doc.meta.get("filename", "Unknown")
            preview = doc.content[:200].replace('\n', ' ')
            print_on_gui(f"{i}. {filename}: {preview}...")

    #clean up
    gui.submit["state"] = "normal"
    gui.entry["state"] = "normal"
    
    gui.delete_bar()

    print_on_gui("\nNew Question: ")

def handle_delete(filename):
    global indexing_pipeline, indexed_files

    if indexing_pipeline is None:
        return
    
    store = indexing_pipeline.get_component("writer").document_store
    docs = store.filter_documents(
        filters={"field": "meta.filename", "operator": "==", "value": filename}
    )
    if not docs:
        print_on_gui(f"No embeddings found for {filename}")
        return
    
    ids = [doc.id for doc in docs]
    store.delete_documents(ids)

    store.save_to_disk(STORE_PATH)

    indexed_files.discard(filename)
    HASH_PATH.write_text(compute_docs_hash())
    print_on_gui(f"File '{filename}' deleted and removed from memory.")

#RAG functions
def load_documents(docs_dir: Path, only_new=False) -> list[Document]:
    documents = []
    if not docs_dir.exists():
        print_on_gui(f"Creating {docs_dir} directory...")
        docs_dir.mkdir(parents=True, exist_ok=True)
        print_on_gui(f"Please add .txt, .docx, or .pdf files to {docs_dir} and run again.")
        return documents

    for file_path in docs_dir.iterdir():
        if file_path.suffix.lower() not in ['.txt', '.pdf', '.docx']:
            continue
        if only_new and file_path.name in indexed_files:
            continue
        try:
            if file_path.suffix.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file_path.suffix.lower() == '.pdf':
                reader = PdfReader(file_path)
                content = '\n'.join(page.extract_text() for page in reader.pages)
            else:
                docx_module = importlib.import_module("docx")
                document = docx_module.Document(file_path)
                content = '\n'.join(para.text for para in document.paragraphs)

            if content.strip():
                documents.append(Document(content=content, meta={"filename": file_path.name}))
                indexed_files.add(file_path.name)

        except Exception as e:
            print_on_gui(f"✗ Error loading {file_path.name}: {e}")

    gui.print_docs(documents)

    print_on_gui(f"\nTotal: {len(documents)} documents loaded")
    return documents


def create_indexing_pipeline(document_store: InMemoryDocumentStore):
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("splitter", DocumentSplitter(split_by="word", split_length=500, split_overlap=50))
    indexing_pipeline.add_component("embedder", SentenceTransformersDocumentEmbedder(model=EMBEDDING_MODEL))
    indexing_pipeline.add_component("writer", DocumentWriter(document_store=document_store))
    indexing_pipeline.connect("splitter.documents", "embedder.documents")
    indexing_pipeline.connect("embedder.documents", "writer.documents")
    return indexing_pipeline


def create_rag_pipeline(document_store: InMemoryDocumentStore):
    template = """
    Answer the question based on the provided context. If you cannot answer based on the context, say so.

    Context:
    {% for doc in documents %}
    {{ doc.content }}
    {% endfor %}

    Question: {{ question }}

    Answer:
    """
    rag_pipeline = Pipeline()
    rag_pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder(model=EMBEDDING_MODEL))
    rag_pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store=document_store, top_k=TOP_K))
    rag_pipeline.add_component("prompt_builder", PromptBuilder(template=template, required_variables=["documents", "question"]))
    rag_pipeline.add_component("llm", OllamaGenerator(model=OLLAMA_MODEL, url="http://localhost:11434"))
    rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    rag_pipeline.connect("retriever.documents", "prompt_builder.documents")
    rag_pipeline.connect("prompt_builder", "llm")
    return rag_pipeline


def rag_load():
    global NEW_DOC, rag_pipeline, indexing_pipeline

    current_hash = compute_docs_hash()
    cached_hash = HASH_PATH.read_text() if HASH_PATH.exists() else None
    
    gui.update_bar(10)

    gui.load_logs()
    
    print_on_gui("=" * 60)
    print_on_gui("Haystack + Ollama RAG Pipeline")
    print_on_gui("=" * 60)
    print_on_gui("\n[1/3] Loading documents...")
    
    
    if STORE_PATH.exists() and cached_hash == current_hash:
        gui.update_bar(10) #20%

        print_on_gui("[2/3] Docs chache detected. Loading cached embeddings...")
        document_store = InMemoryDocumentStore.load_from_disk(STORE_PATH)
        print_on_gui("Cache Loaded")
        indexing_pipeline = create_indexing_pipeline(document_store)
        gui.update_bar(30) #50%
        for file in DOCS_DIR.iterdir():
            indexed_files.add(file.name)

    else:
        document_store = InMemoryDocumentStore()
    
        gui.update_bar(20) #30%
        documents = load_documents(DOCS_DIR, only_new=False)
        if not documents:
            print_on_gui("\nNo documents found. Add .pdf, .docx, or .txt files to ../docs/ directory.")
            return
    
        gui.update_bar(10) #40%

        print_on_gui(f"\n[2/3] Indexing documents (this may take a minute on first run)...")
        indexing_pipeline = create_indexing_pipeline(document_store)
    

        gui.update_bar(10) #50%

        indexing_pipeline.run({"splitter": {"documents": documents}})
        print_on_gui(f"✓ Indexed {document_store.count_documents()} document segments")

        document_store.save_to_disk(STORE_PATH)
        HASH_PATH.write_text(current_hash)
        print_on_gui("Embeddings cached.")
    
    gui.update_bar(20) #70%


    # Create RAG pipeline
    print_on_gui("\n[3/3] Creating RAG pipeline...")
    rag_pipeline = create_rag_pipeline(document_store)
    gui.update_bar(29.9) #100%

    print_on_gui("✓ Pipeline ready!")

    print_on_gui("\n" + "=" * 60)
    print_on_gui("Ask questions about your documents (type 'quit' to exit)")
    print_on_gui("=" * 60 + "\n")


    print_on_gui("\nQuestion: ")

    gui.delete_bar()
    
def main():
    global gui
    gui = GUI(on_submit=handle_submit, on_upload=get_file, on_start=rag_load, on_delete=handle_delete)
    print_on_gui("Loading... \n\n")
    gui.progressive_bar()

    gui.root.after(100, gui.start_load)
    gui.run()

if __name__ == "__main__":
    main()
