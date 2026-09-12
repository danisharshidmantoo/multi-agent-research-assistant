from .chunker import DocumentChunker
from .document_loader import DocumentLoader
from .embeddings import EmbeddingModel
from .vector_store import VectorStore


class IngestionPipeline:
    def __init__(
        self,
        document_directory: str = "data/documents",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: str = "all-MiniLM-L6-v2",
        chroma_directory: str = "data/chroma",
        collection_name: str = "documents",
    ):
        self.loader = DocumentLoader(document_directory)

        self.chunker = DocumentChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        self.embedding_model = EmbeddingModel(
            model_name=embedding_model
        )

        self.vector_store = VectorStore(
            persist_directory=chroma_directory,
            collection_name=collection_name,
        )

    def ingest(self):
        documents = self.loader.load_documents()

        chunks = self.chunker.split_documents(documents)

        embeddings = self.embedding_model.embed_documents(
            chunks
        )

        self.vector_store.add_documents(
            chunks,
            embeddings,
        )

        return {
            "documents": len(documents),
            "chunks": len(chunks),
        }