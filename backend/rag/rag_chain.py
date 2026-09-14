import time

from langchain_core.prompts import ChatPromptTemplate

from backend.rag.retriever import create_retriever
from backend.rag.llm import create_llm
from backend.rag.source_handler import (
    create_source_info,
    format_sources,
)


RAG_PROMPT = """
You are NovaTech's Leave Policy AI Assistant.

Answer using ONLY the leave policy context.

Do not guess or use outside knowledge.

If the answer is not available, say:
"I couldn't find this information in the leave policy."

Give a clear and concise answer.

Leave Policy Context:
{context}

User Question:
{question}

Answer:
"""


def format_documents(documents):
    documents_text = []

    for document in documents:
        page = document.metadata.get("page")

        if page is not None:
            page += 1

        documents_text.append(
            f"[Policy Page {page}]\n{document.page_content}"
        )

    return "\n\n".join(documents_text)


def ask_question(question):
    total_start = time.perf_counter()

    # ---------------------------------------------------------
    # Load cached Retriever and LLM
    # ---------------------------------------------------------

    retriever = create_retriever()
    llm = create_llm()

    # ---------------------------------------------------------
    # Retrieval Timing
    # ---------------------------------------------------------

    retrieval_start = time.perf_counter()

    documents = retriever.invoke(question)

    retrieval_time = time.perf_counter() - retrieval_start

    # ---------------------------------------------------------
    # Context Preparation
    # ---------------------------------------------------------

    context_start = time.perf_counter()

    context = format_documents(documents)

    prompt = ChatPromptTemplate.from_template(
        RAG_PROMPT
    )

    context_time = time.perf_counter() - context_start

    # ---------------------------------------------------------
    # Groq LLM Timing
    # ---------------------------------------------------------

    llm_start = time.perf_counter()

    response = (prompt | llm).invoke(
        {
            "context": context,
            "question": question,
        }
    )

    llm_time = time.perf_counter() - llm_start

    # ---------------------------------------------------------
    # Source Processing
    # ---------------------------------------------------------

    source_start = time.perf_counter()

    sources = create_source_info(documents)

    if (
        "all leave" in question.lower()
        or "leave policy names" in question.lower()
    ):
        for source in sources:
            if source["section"] == "Types of Leave":
                sources = [source]
                break

    if sources:
        sources = sources[:1]

    formatted_sources = format_sources(sources)

    source_time = time.perf_counter() - source_start

    # ---------------------------------------------------------
    # Total Timing
    # ---------------------------------------------------------

    total_time = time.perf_counter() - total_start

    print("\n" + "=" * 50)
    print(f"Question       : {question}")
    print(f"Retrieval Time : {retrieval_time:.2f} sec")
    print(f"Context Time   : {context_time:.2f} sec")
    print(f"Groq LLM Time  : {llm_time:.2f} sec")
    print(f"Source Time    : {source_time:.2f} sec")
    print(f"TOTAL TIME     : {total_time:.2f} sec")
    print("=" * 50)

    return {
        "answer": response.content,
        "sources": sources,
        "formatted_sources": formatted_sources,
    }


if __name__ == "__main__":
    question = "How many days of Earned Leave do employees get?"

    result = ask_question(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    print(result["formatted_sources"])