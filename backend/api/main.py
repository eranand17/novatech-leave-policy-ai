from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.rag.rag_chain import ask_question
from backend.rag.retriever import create_retriever
from backend.rag.llm import create_llm


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="NovaTech Leave Policy AI",
    description="RAG-based Leave Policy Assistant",
    version="1.0.0",
)

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    sources: list


@app.on_event("startup")
def warmup_rag():
    print("\nStarting NovaTech Leave Policy AI...")
    print("Loading RAG models...")

    create_retriever()
    create_llm()

    print("RAG models loaded successfully.")
    print("Server is ready for questions.\n")


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/ask", response_model=QuestionResponse)
def ask_leave_policy(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }

    result = ask_question(question)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
    }