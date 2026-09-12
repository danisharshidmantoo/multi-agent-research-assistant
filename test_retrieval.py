from rag.embeddings import EmbeddingModel
from rag.retriever import RAGRetriever
from rag.vector_store import VectorStore


embedding_model = EmbeddingModel()
vector_store = VectorStore()

retriever = RAGRetriever(
    embedding_model,
    vector_store,
)

results = retriever.retrieve(
    "What is retrieval augmented generation?",
    top_k=3,
)

for result in results:
    print("\n---")
    print("Content:")
    print(result["content"])
    print("Metadata:")
    print(result["metadata"])
    print("Distance:")
    print(result["distance"])