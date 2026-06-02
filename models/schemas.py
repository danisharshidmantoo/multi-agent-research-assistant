from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=300, description="Research topic")


class AgentOutputs(BaseModel):
    research_notes: str
    analysis_report: str
    summary_report: str


class ResearchResponse(BaseModel):
    topic: str
    result: AgentOutputs


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "multi-agent-research-assistant"

