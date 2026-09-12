import asyncio

from rag.research_paper_tool import search_research_papers
from services.llm_service import LLMService


async def main():
    llm = LLMService()

    result = await llm.generate_with_tools(
        """
        Research the topic of retrieval augmented generation.

        Use the research paper search tool if it is useful.
        Give me a concise answer based on the information you find.
        """,
        tools=[search_research_papers],
    )

    print(result)


asyncio.run(main())