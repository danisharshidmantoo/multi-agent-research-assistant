import hashlib

import chromadb


class VectorStore:
    def __init__(
        self,
        persist_directory: str = "data/chroma",
        collection_name: str = "documents",
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def _create_chunk_id(self, document, index: int) -> str:
        source = document.metadata.get("source", "unknown")
        raw_id = f"{source}_{index}"

        return hashlib.sha256(
            raw_id.encode("utf-8")
        ).hexdigest()

    def add_documents(self, documents, embeddings):
        ids = [
            self._create_chunk_id(document, index)
            for index, document in enumerate(documents)
        ]

        self.collection.upsert(
            ids=ids,
            documents=[
                document.page_content
                for document in documents
            ],
            embeddings=embeddings.tolist(),
            metadatas=[
                document.metadata
                for document in documents
            ],
        )
    def search(self, query_embedding, top_k: int = 5):
        return self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
                ],
             )