from services.llm_service import LLMService


class SummaryAgent:
    """
    SummaryAgent creates a concise executive report from analysis.
    It focuses on clarity, brevity, and final recommendations.
    """

    def __init__(self, llm_service: LLMService) -> None:
        self._llm_service = llm_service

    async def run(self, topic: str, analysis_report: str) -> str:
        prompt = f"""
You are an executive communications specialist.
Summarize the analysis for topic "{topic}" into a concise final report.

Include:
- Executive summary (3-4 bullets)
- Most important trends
- Recommended next steps

Keep it compact, practical, and easy for decision-makers.

Analysis Report:
{analysis_report}
"""
        return await self._llm_service.generate(prompt.strip())

