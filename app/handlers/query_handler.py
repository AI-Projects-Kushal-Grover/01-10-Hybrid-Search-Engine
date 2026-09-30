from app.domain.models import QueryRequest, QueryResult
from app.services import keyword_search, semantic_search

class QueryHandler():
    async def search(self, query: QueryRequest) -> QueryResult:
        results_semantic = await semantic_search.search(query.search, query.operator, query.normalize_embeddings)
        results_keywords = keyword_search.search(query.search)
        return results_semantic
