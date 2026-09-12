import asyncio

from rag.research_paper_tool import search_research_papers
from services.gemini_service import GeminiService


async def main():
    gemini = GeminiService()

    result = await gemini.generate_with_tools(
        """
        Research the topic of retrieval augmented generation.
        Use the research paper search tool if it is useful.
        Give me a concise answer based on the information you find.
        """,
        tools=[search_research_papers],
    )

    print(result)


asyncio.run(main())