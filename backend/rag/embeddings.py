from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


PDF_PATH = Path(__file__).resolve().parents[2] / "data" / "leave_policy.pdf"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


def load_documents():
    """Load the leave policy PDF."""

    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()

    return documents


def split_documents(documents):
    """Split PDF documents into smaller chunks."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def create_embeddings():
    """Create the Hugging Face embedding model."""

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    return embeddings


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    embeddings = create_embeddings()

    test_embedding = embeddings.embed_query(
        "How many Earned Leaves do I get?"
    )

    print(f"Total pages loaded: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print(f"Embedding dimension: {len(test_embedding)}")
    print("\nEmbedding created successfully.")