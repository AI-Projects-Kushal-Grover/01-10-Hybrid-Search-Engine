from app.domain.models import DocumentResult, MergeStrategy

class HybridMerge():
    @staticmethod
    def merge_results(merge_strategy: MergeStrategy, results_semantic: list[DocumentResult], results_keywords: list[DocumentResult]) -> list[DocumentResult]:
        results: list[DocumentResult] = []
        match merge_strategy:
            case "candidiate_merging":
                results = []
            case "score_normalization":
                results = []
            case "rrf":
                results = []
        
        return results
