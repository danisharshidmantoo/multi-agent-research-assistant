# 🤖 Multi-Agent Research Assistant

> A production-style AI research backend combining **multi-agent orchestration, RAG, tool calling, and LLM provider abstraction**.

Built with **Python, FastAPI, Gemini, Groq, ChromaDB, and Docker**.

---

## 🧠 How It Works

```mermaid
flowchart TD
    U[User Topic] --> API[FastAPI /research]
    API --> O[Orchestrator]

    O --> R[Research Agent]
    R --> LLM[LLM Service]
    R -. Optional Tool Call .-> RAG[Research Paper RAG]

    RAG --> E[Embeddings]
    E --> C[ChromaDB]

    LLM --> G[Gemini]
    LLM --> Q[Groq Fallback]

    R --> RN[Research Notes]
    RN --> A[Analysis Agent]
    A --> AR[Analysis Report]
    AR --> S[Summary Agent]
    S --> SR[Summary Report]

    SR --> O
    O --> API
    API --> U

    Agent Pipeline

Research → Analysis → Summary

Agent	Responsibility
🔎 Research Agent	Generates detailed research and can optionally retrieve relevant research papers through RAG
📊 Analysis Agent	Extracts insights, trends, risks, and actionable takeaways
📝 Summary Agent	Produces an executive summary and recommendations
🎯 Orchestrator Agent	Coordinates the complete workflow and combines the outputs

RAG is available only to the Research Agent. Analysis and Summary operate on the outputs produced by the preceding stages.

⚙️ Key Engineering Highlights
Multi-Agent Architecture — Specialized agents coordinated through a centralized Orchestrator.
RAG + Tool Calling — Research Agent can dynamically invoke a research-paper retrieval tool when indexed knowledge is useful.
Semantic Retrieval — Documents are chunked, embedded with all-MiniLM-L6-v2, and stored in ChromaDB.
LLM Abstraction — Agent logic is decoupled from individual model providers through a unified LLMService.
Provider Fallback — Gemini and Groq provide interchangeable backends with automatic fallback handling.
Production-Oriented Backend — FastAPI API layer, configuration management, error handling, timeouts, logging, and Docker support.
🔍 RAG Pipeline
Research Papers
      ↓
Document Loading
      ↓
Chunking
      ↓
Embeddings
      ↓
ChromaDB
      ↓
Semantic Retrieval
      ↓
Research Agent

The LLM decides whether to use the research-paper retrieval tool based on the research task.

🚀 API
POST /research

Request

{
  "topic": "Future of AI in healthcare"
}

Response

{
  "topic": "Future of AI in healthcare",
  "result": {
    "research_notes": "...",
    "analysis_report": "...",
    "summary_report": "..."
  }
}
GET /health

Service health check.

🛠️ Tech Stack

Python · FastAPI · Gemini · Groq · RAG · ChromaDB · Sentence Transformers · LangChain · Docker

📁 Project Structure
multi-agent-research-assistant/
├── agents/
│   ├── orchestrator_agent.py
│   ├── research_agent.py
│   ├── analysis_agent.py
│   └── summary_agent.py
├── api/
│   └── routes.py
├── models/
├── rag/
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── research_paper_tool.py
│   └── pipeline.py
├── services/
│   ├── llm_service.py
│   ├── gemini_service.py
│   ├── groq_service.py
│   └── config.py
├── Dockerfile
├── main.py
├── requirements.txt
└── .env.example
⚡ Getting Started
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
uvicorn main:app --reload

API documentation:

http://127.0.0.1:8000/docs

Environment
LLM_PRIMARY_PROVIDER=gemini

GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
🐳 Docker
docker build -t multi-agent-research-assistant .
docker run --rm -p 8000:8000 --env-file .env multi-agent-research-assistant
🔮 Future Improvements
Authentication & rate limiting
Agent and API test coverage
Observability with metrics and tracing
Persistent research history
CI/CD pipeline