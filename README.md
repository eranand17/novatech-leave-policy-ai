# NovaTech Leave Policy AI

An AI-powered **Retrieval-Augmented Generation (RAG)** chatbot that answers employee questions using the NovaTech Leave & Attendance Policy.

The application retrieves relevant information from the official policy document and generates concise, policy-grounded answers with source references.

## Features

* 📄 PDF-based Leave Policy knowledge base
* 🔎 Semantic search using FAISS
* 🧠 HuggingFace embeddings
* 🤖 Retrieval-Augmented Generation (RAG)
* ⚡ Groq-powered LLM responses
* 📚 Source and page references
* 🚀 FastAPI backend
* 💻 Responsive web interface
* 📱 Mobile-friendly design
* ⚡ Cached RAG models for faster responses
* 🛡️ Answers generated using retrieved policy context only

## Tech Stack

### Backend

* Python
* FastAPI
* LangChain
* Groq

### AI / RAG

* HuggingFace Embeddings
* FAISS Vector Database
* Retrieval-Augmented Generation (RAG)
* Groq LLM

### Frontend

* HTML5
* CSS3
* JavaScript

### Data

* PDF
* SQLite / local project data where applicable

## System Architecture

```text
User Question
      ↓
FastAPI API
      ↓
Question Processing
      ↓
FAISS Similarity Search
      ↓
Relevant Policy Chunks
      ↓
RAG Context
      ↓
Groq LLM
      ↓
Answer + Source Reference
```

## How RAG Works

1. The NovaTech Leave Policy PDF is loaded into the application.
2. The document is divided into smaller text chunks.
3. HuggingFace embeddings convert the chunks into vector representations.
4. The vectors are stored in a FAISS vector database.
5. When a user asks a question, FAISS retrieves the most relevant policy chunks.
6. The retrieved context is passed to the Groq LLM.
7. The LLM generates a concise answer based on the retrieved policy information.
8. The application returns the answer along with the relevant source reference.

## Project Structure

```text
novatech-leave-policy-ai/
│
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── llm.py
│   │   ├── pdf_loader.py
│   │   ├── rag_chain.py
│   │   ├── retriever.py
│   │   ├── source_handler.py
│   │   ├── text_splitter.py
│   │   └── vector_store.py
│   │
│   └── __init__.py
│
├── data/
│   └── leave_policy.pdf
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── index.html
│
├── .gitignore
├── README.md
├── requirements.txt
├── retriever_test.txt
└── run.ps1
```

## Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/eranand17/novatech-leave-policy-ai.git
cd novatech-leave-policy-ai
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit API keys or other sensitive credentials to GitHub.

## Run the Application

Start the FastAPI server:

```powershell
uvicorn backend.api.main:app --reload
```

Open the application in your browser:

```text
http://127.0.0.1:8000
```

## API

### POST `/ask`

Send a question to the RAG assistant.

Example request:

```json
{
  "question": "Who approves leave?"
}
```

Example response:

```json
{
  "answer": "Leave is normally approved by your reporting manager. For longer or special types of leave, HR approval may also be required.",
  "sources": [
    {
      "section": "Leave Approval",
      "page": 7
    }
  ]
}
```

## Example Questions

The assistant can answer questions such as:

* What is Earned Leave?
* How many days of Earned Leave do employees get?
* Who approves leave?
* How many days in advance should leave be applied for?
* Can Earned Leave be carried forward?
* What types of leave are available?
* What is the leave cancellation policy?

## Performance

The application uses **startup warm-up and caching** for the RAG components to reduce first-request latency.

Typical response times after startup:

```text
Retrieval:   ~0.04 - 0.05 seconds
LLM:         ~0.7 - 1.3 seconds
Total:       ~0.7 - 1.3 seconds
```

The embedding model is loaded during application startup, avoiding the initial model-loading delay when the first question is submitted.

## Testing

The RAG retrieval pipeline has been tested with multiple policy-related questions covering:

* Earned Leave
* Leave approval
* Leave application
* Carry-forward rules
* Policy-specific information retrieval

The application was also tested for response speed and answer quality.

## Security

* API credentials are stored using environment variables.
* `.env` files are excluded using `.gitignore`.
* No API keys should be committed to the repository.
* The LLM is instructed to answer using the retrieved policy context.

## Future Improvements

* Cloud deployment
* User authentication
* Conversation history
* Multiple policy document support
* Admin interface for policy updates
* Improved citation and source handling
* Advanced Agentic RAG capabilities

## Author

**Anand Kumar Singh**

B.Tech Computer Science Engineering Student

### Areas of Interest

* Python
* Django
* Generative AI
* LLMs
* RAG
* AI Engineering

## License

This project is created for educational and portfolio purposes.
