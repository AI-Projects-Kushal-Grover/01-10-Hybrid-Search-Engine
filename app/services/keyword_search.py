import BM25

from app.domain.models import Document, DocumentResult, QueryResult
from app.repositories.document_chunk import DocumentChunkRepository

class KeywordSearch():
    def __init__(self) -> None:
        self.document_chunk_repository = DocumentChunkRepository()
        self.retriever: BM25.BM25Search | None = None
        self.document_corpus: list[tuple] = []

    async def index_keywords(self):
        document_chunks = await self.document_chunk_repository.select_all()
        corpus: list[str] = []
        for document in document_chunks:
            formatted = f"{document[1]} {document[2]}"
            corpus.append(formatted)
            self.document_corpus.append((*document, formatted))
        self.retriever = BM25.index(corpus)

    def search(self, query: str, limit = 5) -> QueryResult:
        if (self.retriever is None):
            raise AttributeError("Value is not initalized yet", name="retriever")

        documents = []
        results = self.retriever.search([query], k=limit)
        for result in results:
            document = list(filter(lambda doc: doc[3] == result, self.document_corpus))[0]
            documents.append(document)
        return QueryResult(documents=documents)
