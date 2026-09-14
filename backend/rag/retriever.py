from pathlib import Path
import re
from functools import lru_cache

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parents[2]
VECTOR_STORE = BASE_DIR / "vector_store"
MODEL = "BAAI/bge-small-en-v1.5"


TOPICS = {
    "earned leave": ["earned leave", "el", "carry forward"],
    "casual leave": ["casual leave", "cl"],
    "sick leave": ["sick leave", "sl", "medical"],
    "optional holiday": ["optional holiday", "oh"],
    "bereavement leave": ["bereavement"],
    "paternity leave": ["paternity"],
    "maternity leave": ["maternity"],
    "compensatory off": ["compensatory off", "comp-off"],
    "leave without pay": ["leave without pay", "lwp"],

    "types of leave": [
        "types of leave",
        "leave types",
        "leave categories",
        "how many types",
        "how many kinds",
        "all leave",
        "all leaves",
        "all leave policy",
        "all leave policies",
        "leave names",
        "mention all leave",
        "list all leave",
        "give me all leave",
    ],

    "leave application": [
        "leave application",
        "apply for leave",
        "hrms",
    ],

    "leave approval": [
        "leave approval",
        "who approves leave",
        "who normally approves",
        "manager approval",
        "reporting manager",
    ],

    "leave cancellation": [
        "cancel approved leave",
        "cancel leave",
        "leave cancellation",
        "cancellation of leave",
    ],

    "probation": ["probation"],
    "emergency leave": ["emergency leave"],
    "public holidays": ["public holidays"],
}


def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


@lru_cache(maxsize=1)
def get_embeddings():
    """
    Load the embedding model only once.

    The model remains cached in memory and is reused
    for every subsequent request.
    """
    return HuggingFaceEmbeddings(
        model_name=MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


@lru_cache(maxsize=1)
def load_store():
    """
    Load the FAISS vector store only once.

    Subsequent calls return the already-loaded store.
    """
    return FAISS.load_local(
        str(VECTOR_STORE),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def word_match(word, text):
    if " " in word:
        return word in text

    return bool(re.search(rf"\b{re.escape(word)}\b", text))


def get_topic(question):
    question = clean(question)

    for topic, words in TOPICS.items():
        for word in words:
            if word_match(word, question):
                return topic

    return None


class Retriever:

    def __init__(self):
        self.store = load_store()

    def invoke(self, question):
        docs = self.store.similarity_search(question, k=8)

        topic = get_topic(question)

        if topic == "types of leave":
            matched = [
                doc
                for doc in docs
                if "types of leave" in clean(doc.page_content)
            ]

            if matched:
                return matched[:4]

        if topic == "leave cancellation":
            matched = [
                doc
                for doc in docs
                if "leave cancellation" in clean(doc.page_content)
                or "cancel approved leave" in clean(doc.page_content)
            ]

            if matched:
                return matched[:4]

        if topic == "leave approval":
            matched = [
                doc
                for doc in docs
                if "leave approval" in clean(doc.page_content)
                or "reporting manager" in clean(doc.page_content)
            ]

            if matched:
                return matched[:4]

        if topic:
            words = TOPICS[topic]

            matched = [
                doc
                for doc in docs
                if any(
                    word_match(word, clean(doc.page_content))
                    for word in words
                )
            ]

            if matched:
                docs = matched

        return docs[:4]


@lru_cache(maxsize=1)
def create_retriever():
    """
    Create the Retriever only once.

    The same Retriever instance is reused across requests.
    """
    return Retriever()