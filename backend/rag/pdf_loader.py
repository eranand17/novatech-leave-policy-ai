from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


PDF_PATH = Path(__file__).resolve().parents[2] / "data" / "leave_policy.pdf"


def load_documents():
    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Total pages loaded: {len(documents)}")

    print("\nFirst page content:\n")
    print(documents[0].page_content[:1000])

    print("\nFirst page metadata:\n")
    print(documents[0].metadata)