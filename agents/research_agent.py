from services.llm_service import LLMService
from rag.research_paper_tool import search_research_papers


class ResearchAgent:
    def __init__(self, llm_service: LLMService) -> None:
        self._llm_service = llm_service

    async def run(self, topic: str) -> str:
        prompt = f"""
You are a senior research specialist.
Create detailed research notes for the topic: "{topic}".

Requirements:
- Cover key concepts, context, recent trends, and practical implications.
- Include potential challenges, opportunities, and future outlook.
- Use structured sections with concise bullet points.
- Keep response factual and specific.

Tool-use rules:
- Use the research paper search tool only when the topic requires
  information that is likely to be found in the indexed research papers.
- Use the tool for research-oriented questions, recent developments,
  scientific findings, research comparisons, or specialized information.
- Do not use the tool for simple arithmetic, basic calculations,
  casual questions, or straightforward general-knowledge questions
  that can be answered reliably without research papers.
- Do not use the tool merely because it is available.
- When the tool is useful, you may call it multiple times with
  different focused queries before producing the final answer.
"""

        return await self._llm_service.generate_with_tools(
            prompt.strip(),
            tools=[search_research_papers],
        )