from app.domain.models import QueryRequest, QueryResult
from app.services.keyword_search import KeywordSearch
from app.services.semantic_search import SemanticSearch

class QueryHandler():
    def __init__(self) -> None:
        self.keyword_search = KeywordSearch()
        self.semantic_search = SemanticSearch()

    async def search(self, query: QueryRequest) -> QueryResult:
        results_semantic = await self.semantic_search.search(query.search, query.operator, query.normalize_embeddings)
        results_keywords = self.keyword_search.search(query.search)
        return results_semantic
