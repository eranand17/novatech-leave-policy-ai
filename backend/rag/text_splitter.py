from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_PATH = Path(__file__).resolve().parents[2] / "data" / "leave_policy.pdf"

def load_documents():
    """Load the leave policy PDF page by page."""

    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()

    return documents

def split_documents(documents):
    """Split documents into smaller chunks for RAG."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks

if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Total pages loaded: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")

    print("\nFirst chunk:\n")
    print(chunks[0].page_content)

    print("\nFirst chunk metadata:\n")
    print(chunks[0].metadata)