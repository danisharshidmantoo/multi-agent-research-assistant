import asyncio

from agents.research_agent import ResearchAgent
from services.llm_service import LLMService


async def main():
    llm_service = LLMService()
    research_agent = ResearchAgent(llm_service)

    result = await research_agent.run(
        "retrieval augmented generation"
    )

    print(result)


asyncio.run(main())