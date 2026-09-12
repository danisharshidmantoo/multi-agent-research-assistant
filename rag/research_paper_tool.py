from rag.embeddings import EmbeddingModel
from rag.retriever import RAGRetriever
from rag.vector_store import VectorStore


class ResearchPaperTool:
    def __init__(self):
        embedding_model = EmbeddingModel()
        vector_store = VectorStore()

        self.retriever = RAGRetriever(
            embedding_model,
            vector_store,
        )

    def search(self, query: str, top_k: int = 3) -> str:
        results = self.retriever.retrieve(
            query,
            top_k=top_k,
        )

        if not results:
            return "No relevant information was found in the research paper database."

        return "\n\n".join(
            result["content"]
            for result in results
        )


research_paper_tool = ResearchPaperTool()


def search_research_papers(query: str) -> str:
    """
    Search the indexed research paper collection for
    information relevant to the given query.
    """
    print(f"\nRAG TOOL CALLED: {query}\n")

    return research_paper_tool.search(query)