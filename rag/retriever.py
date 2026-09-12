from .embeddings import EmbeddingModel
from .vector_store import VectorStore


class RAGRetriever:
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5):
        query_embedding = self.embedding_model.embed_query(query)

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k,
        )

        retrieved_documents = []

        for i, content in enumerate(results["documents"][0]):
            retrieved_documents.append(
                {
                    "content": content,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                }
            )

        return retrieved_documents