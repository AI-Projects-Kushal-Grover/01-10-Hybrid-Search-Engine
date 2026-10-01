from app.domain.models import DocumentResult, MergeStrategy
from app.services.merge_strategies import get_merge_strategy

class HybridMerge():
    @staticmethod
    def merge_results(merge_strategy: MergeStrategy, results_semantic: list[DocumentResult], results_keywords: list[DocumentResult]) -> list[DocumentResult]:
        results: list[DocumentResult] = []
        strategy_class = get_merge_strategy(merge_strategy)
        if strategy_class:
            results = strategy_class.merge(results_semantic, results_keywords)
        
        return results
