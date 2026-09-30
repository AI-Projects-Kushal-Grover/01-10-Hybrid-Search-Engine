import BM25

from app.domain.models import DocumentResult, QueryResult
from app.repositories import document_chunk_repository

class KeywordSearch():
    def __init__(self) -> None:
        self.retriever: BM25.BM25Search | None = None
        self.document_corpus: list[tuple] = []

    async def index_keywords(self):
        document_chunks = await document_chunk_repository.select_all()
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
        for result in results[0]:
            document = list(filter(lambda doc: doc[3] == result["document"], self.document_corpus))[0]
            documents.append(DocumentResult(id = document[0], title=document[1], content=document[2], distance=result["score"]))
        return QueryResult(documents=documents)
