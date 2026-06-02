from fastapi import FastAPI

from api.routes import router as research_router
from services.logger import setup_logging


setup_logging()

app = FastAPI(
    title="Multi-Agent Research Assistant",
    version="1.0.0",
    description=(
        "Production-style FastAPI backend with Research, Analysis, Summary, and "
        "Orchestrator agents; Gemini integration with Groq fallback; Docker-ready."
    ),
)

app.include_router(research_router)

