from typing import List

from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

class Embedder():
    def __init__(self) -> None:
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    def embed(self, chunks: List[str], normalize_embeddings = True) -> list[list[float]]:
        return self.embedding_model.encode(chunks, normalize_embeddings=normalize_embeddings).tolist()
