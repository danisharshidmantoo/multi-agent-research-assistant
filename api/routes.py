import logging

from fastapi import APIRouter, Depends, HTTPException, status

from agents.orchestrator_agent import OrchestratorAgent
from models.schemas import HealthResponse, ResearchRequest, ResearchResponse
from services.dependencies import get_orchestrator_agent
from services.exceptions import AgentExecutionError, ConfigurationError, GeminiServiceError


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    return HealthResponse()


@router.post(
    "/research",
    response_model=ResearchResponse,
    status_code=status.HTTP_200_OK,
    tags=["research"],
)
async def run_research(
    request: ResearchRequest,
    orchestrator: OrchestratorAgent = Depends(get_orchestrator_agent),
) -> ResearchResponse:
    try:
        result = await orchestrator.run(request.topic)
        return ResearchResponse(topic=request.topic, result=result)
    except ConfigurationError as exc:
        logger.error("Configuration error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error. Check LLM provider environment variables.",
        ) from exc
    except (GeminiServiceError, AgentExecutionError) as exc:
        logger.error("Research flow failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Research pipeline failed while processing request.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected server error.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected internal server error.",
        ) from exc

