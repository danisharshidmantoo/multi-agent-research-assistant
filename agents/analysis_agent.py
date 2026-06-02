from services.llm_service import LLMService


class AnalysisAgent:
    """
    AnalysisAgent interprets research notes to identify core insights and trends.
    It converts raw research into decision-friendly analytical output.
    """

    def __init__(self, llm_service: LLMService) -> None:
        self._llm_service = llm_service

    async def run(self, topic: str, research_notes: str) -> str:
        prompt = f"""
You are an expert strategic analyst.
Analyze the following research notes for topic "{topic}" and extract:
1) Key insights
2) Trend signals
3) Risks and blind spots
4) Actionable takeaways

Research Notes:
{research_notes}

Output in clear markdown sections.
"""
        return await self._llm_service.generate(prompt.strip())

