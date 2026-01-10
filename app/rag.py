import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# ---------------- CONFIG ----------------

PDF_DIR = "./data/pdfs"
CHROMA_DIR = "./data/chroma"

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://host.docker.internal:11434"
)

EMBED_MODEL = "nomic-embed-text"

# ---------------- RAG ----------------

def get_retriever():
    # Ensure folders exist
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(CHROMA_DIR, exist_ok=True)

    # Collect PDFs
    pdf_files = [
        os.path.join(PDF_DIR, f)
        for f in os.listdir(PDF_DIR)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        raise RuntimeError(
            f"No PDFs found in {PDF_DIR}. "
            f"Put at least one PDF there."
        )

    # Load PDFs
    documents = []
    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        documents.extend(loader.load())

    if not documents:
        raise RuntimeError("PDFs loaded but no text extracted.")

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        raise RuntimeError("Text split produced zero chunks.")

    # Create embeddings (NO MODEL CHECK)
    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

    # Build vector store
    db = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )

    return db.as_retriever()
