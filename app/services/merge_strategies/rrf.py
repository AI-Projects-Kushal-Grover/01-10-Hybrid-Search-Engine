from app.domain.models import DocumentResult

k: int = 60

class RRFMergeStrategy:
    @staticmethod
    def merge(results_semantic: list[DocumentResult], results_keywords: list[DocumentResult]) -> list[DocumentResult]:
        merged_results = {}
        for result_list in [results_semantic, results_keywords]:
            for rank, result in enumerate(result_list):
                if result.id not in merged_results:
                    merged_results[result.id] = {
                        "result": result,
                        "score": 0,
                    }
                merged_results[result.id]["score"] += 1 / (k + rank)

        sorted_results = sorted(
            merged_results.values(), key=lambda x: x["score"], reverse=True
        )
        return [item["result"] for item in sorted_results]
