from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

PDF_PATH = BASE_DIR / "data" / "leave_policy.pdf"
VECTOR_STORE_PATH = BASE_DIR / "vector_store"


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# ---------------------------------------------------------
# Load PDF
# ---------------------------------------------------------

def load_documents():
    """Load the leave policy PDF."""

    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"Leave policy PDF not found: {PDF_PATH}"
        )

    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()

    return documents


# ---------------------------------------------------------
# Split Documents
# ---------------------------------------------------------

def split_documents(documents):
    """Split documents into smaller chunks."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


# ---------------------------------------------------------
# Create Embeddings
# ---------------------------------------------------------

def create_embeddings():
    """Create Hugging Face embedding model."""

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        },
    )

    return embeddings


# ---------------------------------------------------------
# Create FAISS Vector Store
# ---------------------------------------------------------

def create_vector_store():
    """Create FAISS vector store from document chunks."""

    print("Loading policy PDF...")
    documents = load_documents()

    print(f"Total pages loaded: {len(documents)}")

    print("Splitting documents...")
    chunks = split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    print("Loading embedding model...")
    embeddings = create_embeddings()

    print("Creating FAISS vector store...")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    print("Saving FAISS vector store...")

    VECTOR_STORE_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    vector_store.save_local(
        str(VECTOR_STORE_PATH)
    )

    print("FAISS vector store created successfully.")

    return vector_store


# ---------------------------------------------------------
# Test Similarity Search
# ---------------------------------------------------------

def test_vector_store(vector_store):
    """Test whether relevant chunks can be retrieved."""

    query = "How many Earned Leaves do I get?"

    print("\nTesting similarity search...")
    print(f"Question: {query}")

    results = vector_store.similarity_search(
        query,
        k=3
    )

    print(f"\nRetrieved chunks: {len(results)}")

    for index, document in enumerate(results, start=1):

        print("\n" + "=" * 60)
        print(f"RESULT {index}")
        print("=" * 60)

        print("\nContent:")
        print(document.page_content)

        print("\nSource:")
        print(document.metadata.get("source"))

        print("Page:")
        print(document.metadata.get("page"))


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    vector_store = create_vector_store()

    test_vector_store(vector_store)