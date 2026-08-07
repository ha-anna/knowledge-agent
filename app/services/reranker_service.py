from sentence_transformers import CrossEncoder

from app.domain.search import SearchResult


class RerankerService:
    def __init__(self):
        self.model = CrossEncoder(
            "BAAI/bge-reranker-v2-m3"
        )

    def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k_rerank: int = 5,
    ) -> list[SearchResult]:

        if not results:
            return []

        pairs = [
            (
                query,
                result.text
            )
            for result in results
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(results, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        reranked = []

        for result, score in ranked[:top_k_rerank]:
            result.rerank_score = float(score)
            reranked.append(result)

        return reranked
