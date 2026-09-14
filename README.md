# NovaTech Leave Policy AI

AI-powered RAG chatbot for answering questions from the NovaTech Leave & Attendance Policy.

## Features

- PDF policy document loading
- Text chunking
- HuggingFace embeddings
- FAISS vector database
- RAG-based question answering
- Groq LLM
- Source and page references
- Simple responsive web interface

## Tech Stack

- Python
- FastAPI
- LangChain
- HuggingFace
- FAISS
- Groq
- HTML
- CSS
- JavaScript

## How It Works

User Question
→ Retriever
→ FAISS Vector Search
→ Relevant Policy Chunks
→ Groq LLM
→ Answer + Sources

## Run Project

Activate virtual environment:

```powershell
.venv\Scripts\activate