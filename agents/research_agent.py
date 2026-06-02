from services.llm_service import LLMService


class ResearchAgent:
    """
    ResearchAgent explores the user topic and gathers detailed information.
    It produces broad and deep source-like notes for downstream agents.
    """

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
"""
        return await self._llm_service.generate(prompt.strip())

