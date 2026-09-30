from app.domain.models import QueryRequest, QueryResult
from app.services import hybrid_merge, keyword_search, semantic_search

class QueryHandler():
    async def search(self, query: QueryRequest) -> QueryResult:
        results_semantic = await semantic_search.search(query.search, query.operator, query.normalize_embeddings)
        results_keywords = keyword_search.search(query.search)
        results_merged = hybrid_merge.merge_results(query.merge_strategy, results_semantic, results_keywords)
        return QueryResult(documents=results_merged)
