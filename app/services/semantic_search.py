from app.domain.entities import DocumentChunk
from app.domain.models import Document, DocumentResult, QueryResult
from app.services.embedder import Embedder
from app.services.chunker import Chunker
from app.repositories import document_chunk_repository

class SemanticSearch():
    def __init__(self) -> None:
        self.embedder = Embedder()

    async def index_document(self, document: Document):
        chunks = Chunker.chunk_fixed_size(document.content, document.chunk_size, document.chunk_overlap)
        embeddings = self.embedder.embed(chunks, document.normalize_embeddings)
        for index, embedding in enumerate(embeddings):
            await document_chunk_repository.insert(DocumentChunk(
                title=document.title,
                content=chunks[index],
                embedding=embedding
            ))

    async def search(self, query: str, operator: str, normalize_embeddings: bool = True) -> QueryResult:
        query_embedding = self.embedder.embed([query], normalize_embeddings)
        document_chunks = await document_chunk_repository.select_by_embeddings(query_embedding[0], operator)
        documents = [DocumentResult(id = document[0], title=document[1], content=document[2], distance=document[3]) for document in document_chunks]
        return QueryResult(documents=documents)
