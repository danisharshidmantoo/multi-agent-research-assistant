from agents.analysis_agent import AnalysisAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.research_agent import ResearchAgent
from agents.summary_agent import SummaryAgent
from services.llm_service import LLMService


def get_orchestrator_agent() -> OrchestratorAgent:
    llm_service = LLMService()
    research_agent = ResearchAgent(llm_service)
    analysis_agent = AnalysisAgent(llm_service)
    summary_agent = SummaryAgent(llm_service)
    return OrchestratorAgent(research_agent, analysis_agent, summary_agent)

