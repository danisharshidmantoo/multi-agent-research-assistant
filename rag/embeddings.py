from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents) -> np.ndarray:
        texts = [document.page_content for document in documents]

        return self.model.encode(
            texts,
            show_progress_bar=True,
        )

    def embed_query(self, query: str) -> np.ndarray:
        return self.model.encode([query])