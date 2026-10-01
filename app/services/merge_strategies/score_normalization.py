from app.domain.models import DocumentResult

class ScoreNormalizationMergeStrategy:
    @staticmethod
    def merge(results_semantic: list[DocumentResult], results_keywords: list[DocumentResult]) -> list[DocumentResult]:
        results = ScoreNormalizationMergeStrategy._prepare_single_list(results_semantic, results_keywords)
        results = ScoreNormalizationMergeStrategy._normalize_scores(results)
        results = ScoreNormalizationMergeStrategy._calculate_hybrid_score(results)
        return sorted(results, key=lambda x: x.hybrid_score, reverse=True)

    @staticmethod
    def _prepare_single_list(results_semantic: list[DocumentResult], results_keywords: list[DocumentResult]):
        results: list[DocumentResult] = results_semantic.copy()
        
        for result in results_keywords:
            if result not in results:
                results.append(result)
            else:
                existing_result = next((r for r in results if r.id == result.id), None)
                if existing_result:
                    existing_result.bm25_score = result.bm25_score
        return results

    @staticmethod
    def _normalize_scores(results: list[DocumentResult]):
        if not results:
            return []

        # Normalize the scores to a range of 0 to 1
        semantic_scores = [result.semantic_score for result in results]
        bm25_scores = [result.bm25_score for result in results]

        min_semantic_score = min(semantic_scores)
        max_semantic_score = max(semantic_scores)

        min_bm25_score = min(bm25_scores)
        max_bm25_score = max(bm25_scores)

        for result in results:
            if min_semantic_score == max_semantic_score:
                result.semantic_score = 1.0
            else:
                result.semantic_score = (result.semantic_score - min_semantic_score) / (max_semantic_score - min_semantic_score)

            if min_bm25_score == max_bm25_score:
                result.bm25_score = 1.0
            else:
                result.bm25_score = (result.bm25_score - min_bm25_score) / (max_bm25_score - min_bm25_score)

        return results

    @staticmethod
    def _calculate_hybrid_score(results: list[DocumentResult]):
        for result in results:
            result.hybrid_score = (result.semantic_score + result.bm25_score) / 2
        return results
