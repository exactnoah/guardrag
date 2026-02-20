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
from pypdf import PdfReader

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
OLLAMA_MODEL = "mistral:7b" 
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3  # Number of documents to retrieve


def load_documents(docs_dir: Path) -> list[Document]:
    """Load text documents from a directory."""
    documents = []
    
    if not docs_dir.exists():
        print(f"Creating {docs_dir} directory...")
        docs_dir.mkdir(parents=True, exist_ok=True)
        print(f"Please add .txt or .pdf files to {docs_dir} and run again.")
        return documents
    
    for file_path in docs_dir.iterdir():
        if file_path.suffix.lower() not in ['.txt', '.pdf']:
            continue

        try:
            if file_path.suffix.lower() == '.txt': # txt
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else: # pdf
                reader = PdfReader(file_path)
                text_parts = [page.extract_text() for page in reader.pages]
                content = '\n'.join(text_parts)
            
            if content.strip(): # check if empty
                documents.append(Document(
                    content=content, 
                    meta={"filename": file_path.name}
                ))
        
        except Exception as e:
            print(f"✗ Error loading {file_path.name}: {e}")
        
    print(f"\nTotal: {len(documents)} documents loaded")
    return documents


def create_indexing_pipeline(document_store: InMemoryDocumentStore):
    """Create a pipeline to embed and store documents."""
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("embedder", SentenceTransformersDocumentEmbedder(model=EMBEDDING_MODEL))
    indexing_pipeline.add_component("writer", DocumentWriter(document_store=document_store))
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


def main():
    print("=" * 60)
    print("Haystack + Ollama RAG Pipeline")
    print("=" * 60)
    
    # Initialize document store
    document_store = InMemoryDocumentStore()
    
    # Load and index documents
    print("\n[1/3] Loading documents...")
    documents = load_documents(DOCS_DIR)
    
    if not documents:
        print("\nNo documents found. Add .pdf or .txt files to ../docs/ directory.")
        return
    
    print(f"\n[2/3] Indexing documents (this may take a minute on first run)...")
    indexing_pipeline = create_indexing_pipeline(document_store)
    indexing_pipeline.run({"embedder": {"documents": documents}})
    print(f"✓ Indexed {document_store.count_documents()} documents")
    
    # Create RAG pipeline
    print("\n[3/3] Creating RAG pipeline...")
    rag_pipeline = create_rag_pipeline(document_store)
    print("✓ Pipeline ready!")
    
    # Interactive Q&A loop
    print("\n" + "=" * 60)
    print("Ask questions about your documents (type 'quit' to exit)")
    print("=" * 60 + "\n")
    
    while True:
        question = input("\nQuestion: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        print("\nThinking...")
        result = rag_pipeline.run({
            "text_embedder": {"text": question},
            "prompt_builder": {"question": question}
        })
        
        answer = result["llm"]["replies"][0]
        print(f"\nAnswer: {answer}")
        
        # Show sources (if available in result)
        if "prompt_builder" in result and "documents" in result["prompt_builder"]:
            retrieved_docs = result["prompt_builder"]["documents"]
            if retrieved_docs:
                print("\n--- Sources ---")
                for i, doc in enumerate(retrieved_docs, 1):
                    filename = doc.meta.get("filename", "Unknown")
                    preview = doc.content[:100].replace('\n', ' ')
                    print(f"{i}. {filename}: {preview}...")


if __name__ == "__main__":
    main()