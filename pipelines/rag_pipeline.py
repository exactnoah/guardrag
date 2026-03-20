"""
Simple RAG Pipeline using Haystack + Ollama
Requires: Ollama running locally with mistral model pulled
"""

import os
from pathlib import Path
from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.writers import DocumentWriter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack.components.preprocessors import DocumentSplitter

from pypdf import PdfReader
from docx import Document as Docxument

from deepeval.models import OllamaModel
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric



#tkinter gui
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import shutil

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
OLLAMA_MODEL = "mistral:7b" 
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 4  # Number of documents to retrieve

NEW_DOC = False
indexed_files = set()
RUNNING = True

#GUI functions
def get_file(event=None):
    filepath = filedialog.askopenfilename()
    filename = os.path.basename(filepath)
    shutil.copy(filepath, f"./docs/{filename}")
    print('Selected: ', filename)
    print_on_gui(f"{filename} added to Docs Folder. Click submit to index and add to pipeline." )

    global NEW_DOC
    NEW_DOC = True

def print_on_gui(*args, sep=" ", end="\n"):
    text = sep.join(map(str, args)) + end
    print(text)

    txt.config(state="normal")
    txt.insert("end", text)
    txt.config(state="disabled")
    txt.see("end")
    root.update_idletasks()





def load_documents(docs_dir: Path, only_new=False) -> list[Document]:
    """Load text documents from a directory."""
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
            if file_path.suffix.lower() == '.txt': # txt
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file_path.suffix.lower() == '.pdf': # pdf
                reader = PdfReader(file_path)
                text_parts = [page.extract_text() for page in reader.pages]
                content = '\n'.join(text_parts)
            else: # docx
                document = Docxument(file_path)
                content = '\n'.join(para.text for para in document.paragraphs)
            
            if content.strip(): # check if empty
                documents.append(Document(
                    content=content, 
                    meta={"filename": file_path.name}
                ))
                indexed_files.add(file_path.name)
        
        except Exception as e:
            print_on_gui(f"✗ Error loading {file_path.name}: {e}")
        
    print_on_gui(f"\nTotal: {len(documents)} documents loaded")
    return documents


def create_indexing_pipeline(document_store: InMemoryDocumentStore):
    """Create a pipeline to embed and store documents."""
    indexing_pipeline = Pipeline()

    indexing_pipeline.add_component("splitter", DocumentSplitter(
        split_by="word",
        split_length=200,
        split_overlap=50
    ))

    indexing_pipeline.add_component("embedder", SentenceTransformersDocumentEmbedder(model=EMBEDDING_MODEL))
    indexing_pipeline.add_component("writer", DocumentWriter(document_store=document_store))
    indexing_pipeline.connect("splitter.documents", "embedder.documents")
    indexing_pipeline.connect("embedder.documents", "writer.documents")
    return indexing_pipeline


def create_rag_pipeline(document_store: InMemoryDocumentStore):
    """Create the RAG pipeline for answering questions."""
    
    # Prompt template
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
    
    # Add components
    rag_pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder(model=EMBEDDING_MODEL))
    rag_pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store=document_store, top_k=TOP_K))
    rag_pipeline.add_component("prompt_builder", PromptBuilder(template=template, required_variables=["documents", "question"]))
    rag_pipeline.add_component("llm", OllamaGenerator(model=OLLAMA_MODEL, url="http://localhost:11434"))
    
    # Connect components
    rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    rag_pipeline.connect("retriever.documents", "prompt_builder.documents")
    rag_pipeline.connect("prompt_builder", "llm")
    
    return rag_pipeline


def rag_load():
    global NEW_DOC, RUNNING

    judge_model = OllamaModel( #declare Ollama as judge
        model=OLLAMA_MODEL,
        base_url="http://localhost:11434"
    )   
    dEMetrics = [
        FaithfulnessMetric(model=judge_model),
        AnswerRelevancyMetric(model=judge_model),
    ]
    print_on_gui("=" * 60)
    print_on_gui("Haystack + Ollama RAG Pipeline")
    print_on_gui("=" * 60)
    
    # Initialize document store
    document_store = InMemoryDocumentStore()
    
    # Load and index documents
    print_on_gui("\n[1/3] Loading documents...")
    documents = load_documents(DOCS_DIR, only_new=False)
    
    if not documents:
        print_on_gui("\nNo documents found. Add .pdf, .docx, or .txt files to ../docs/ directory.")
        return
    
    print_on_gui(f"\n[2/3] Indexing documents (this may take a minute on first run)...")
    indexing_pipeline = create_indexing_pipeline(document_store)
    indexing_pipeline.run({"splitter": {"documents": documents}})
    print_on_gui(f"✓ Indexed {document_store.count_documents()} documents")
    
    # Create RAG pipeline
    print_on_gui("\n[3/3] Creating RAG pipeline...")
    rag_pipeline = create_rag_pipeline(document_store)
    print_on_gui("✓ Pipeline ready!")
    
    # Interactive Q&A loop
    print_on_gui("\n" + "=" * 60)
    print_on_gui("Ask questions about your documents (type 'quit' to exit)")
    print_on_gui("=" * 60 + "\n")


    
    while RUNNING:
        button_pressed.set("False")
        print_on_gui("\nQuestion: ")

        while button_pressed.get() != "True" and RUNNING:
            root.update()

        #catch for closing via gui
        if not RUNNING:
            break

        question = entry.get().strip()
        print_on_gui(question)
        entry.delete(0, tk.END)

        if NEW_DOC:
            print_on_gui("\nNew doc detected, indexing and appending...")
            new_documents = load_documents(DOCS_DIR, only_new=True)

            if new_documents:
                indexing_pipeline.run({"splitter": {"documents": new_documents}})
                print_on_gui("\nNew Document Added")
            else:
                print_on_gui("No new documents found")
            NEW_DOC = False
        
        if question.lower() in ['quit', 'exit', 'q']:
            print_on_gui("Goodbye!")
            root.after(3000, root.destroy)
            break
        
        if not question:
            continue
        
        print_on_gui("\nThinking...")
        result = rag_pipeline.run({
            "text_embedder": {"text": question},
            "prompt_builder": {"question": question}
        },
            include_outputs_from=["retriever"]
        )
        
        answer = result["llm"]["replies"][0]



        
        retrieved_docs = result["retriever"]["documents"]
        
        # Show sources (if available in result)
        if retrieved_docs:
            if evalChecked == 1: 
                testcase = LLMTestCase(
                    input=question,
                    actual_output=answer,
                    retrieval_context = [doc.content for doc in retrieved_docs]
                    )
                answerValid = True
                
                print_on_gui(f"\n\nRe-Evaluating Answer...")

                DEresults = evaluate(
                    test_cases=[testcase],
                    metrics=dEMetrics
                )

                metrics_results = DEresults.test_results[0].metrics_data

                #check if factually correct according to retrieved docs
                if metrics_results[0].score < 0.75: 
                    print_on_gui("\nLikely Halucinations detected. Please try again with a more specific question or after adding relevant files.")
                    print_on_gui(f"Reasoning: {metrics_results[0].reason}")
                    answerValid = False

                #check if answer actually answers question
                if metrics_results[1].score < 0.75: 
                    print_on_gui("\nGenerated Answer may not be relevant to asked question. Please try again with a more specific question or after adding relevant files.")
                    print_on_gui(f"Reasoning: {metrics_results[1].reason}")
                    answerValid = False

                if answerValid:
                    print_on_gui("\n--- Evaluation Results ---")
                    for metric in DEresults.test_results[0].metrics_data:
                        print_on_gui(f"{metric.name}: {metric.score:.2f}")
                        print_on_gui(f"Reasoning: {metric.reason}")


            print_on_gui(f"\nAnswer: {answer}")



            if sourceChecked.get() == 1:
                print_on_gui("\n--- Sources ---")
                for i, doc in enumerate(retrieved_docs, 1):
                    filename = doc.meta.get("filename", "Unknown")
                    preview = doc.content[:200].replace('\n', ' ')
                    print_on_gui(f"{i}. {filename}: {preview}...")


            

def main():
    print_on_gui("Loading... \n\n")
    root.after(4000, rag_load)
    root.mainloop()

def start_loop(event):
    button_pressed.set("True")

def on_close():
    global RUNNING
    RUNNING = False
    root.quit()
    root.destroy()

#tkinter GUI setup
root = tk.Tk()
root.title("GuardRag")
root.minsize(600, 400)
root.geometry("300x300+300+250")

upload_button = tk.Button(root, text="New File", command=get_file)
upload_button.pack(anchor="w")

userInput = tk.StringVar()
entry = tk.Entry(root, width=70)
entry.pack(padx=10, pady=10, anchor="n", fill="x")

button_pressed = tk.StringVar()
btn = tk.Button(root, text="submit", command=lambda: button_pressed.set("True"))
btn.pack(anchor="n")

entry.bind("<Return>", start_loop)

txt = scrolledtext.ScrolledText(root, height=15, wrap="word")
txt.pack(padx=10, pady=10, side=tk.BOTTOM, expand=True, anchor="n", fill="both")

evalChecked = tk.IntVar()
runEval = tk.Checkbutton(root, text="Run DeepEval Check", variable=evalChecked)
runEval.pack(anchor="w")

sourceChecked = tk.IntVar()
showSources = tk.Checkbutton(root, text="Show Sources", variable=sourceChecked)
showSources.pack(anchor="w")


root.protocol("WM_DELETE_WINDOW", on_close)

if __name__ == "__main__":
    main()