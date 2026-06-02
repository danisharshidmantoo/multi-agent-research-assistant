import logging

from agents.analysis_agent import AnalysisAgent
from agents.research_agent import ResearchAgent
from agents.summary_agent import SummaryAgent
from models.schemas import AgentOutputs
from services.exceptions import AgentExecutionError


logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """
    OrchestratorAgent coordinates the complete multi-agent workflow.
    It executes research -> analysis -> summary and returns a unified result.
    """

    def __init__(
        self,
        research_agent: ResearchAgent,
        analysis_agent: AnalysisAgent,
        summary_agent: SummaryAgent,
    ) -> None:
        self._research_agent = research_agent
        self._analysis_agent = analysis_agent
        self._summary_agent = summary_agent

    async def run(self, topic: str) -> AgentOutputs:
        try:
            logger.info("Starting orchestration for topic: %s", topic)
            research_notes = await self._research_agent.run(topic)
            analysis_report = await self._analysis_agent.run(topic, research_notes)
            summary_report = await self._summary_agent.run(topic, analysis_report)
            logger.info("Completed orchestration for topic: %s", topic)

            return AgentOutputs(
                research_notes=research_notes,
                analysis_report=analysis_report,
                summary_report=summary_report,
            )
        except Exception as exc:
            logger.exception("Agent workflow failed for topic: %s", topic)
            raise AgentExecutionError("Agent workflow execution failed.") from exc

