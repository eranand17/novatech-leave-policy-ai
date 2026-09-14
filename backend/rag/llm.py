import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Groq Configuration
# ---------------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-120b"


# ---------------------------------------------------------
# Create Groq LLM
# ---------------------------------------------------------

@lru_cache(maxsize=1)
def create_llm():
    """Create and cache the Groq LLM."""

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not configured. "
            "Please add it to the .env file."
        )

    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=MODEL_NAME,
        temperature=0,
    )


# ---------------------------------------------------------
# Test LLM
# ---------------------------------------------------------

def test_llm():
    """Send a simple test question to the Groq LLM."""

    llm = create_llm()

    question = "What is the purpose of an employee leave policy?"

    response = llm.invoke(question)

    print("Groq LLM test successful.")
    print(f"\nModel: {MODEL_NAME}")
    print(f"\nQuestion:\n{question}")
    print("\nAnswer:")
    print(response.content)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    test_llm()