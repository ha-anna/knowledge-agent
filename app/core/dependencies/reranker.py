from app.services.reranker_service import RerankerService

reranker_service = RerankerService()


def get_reranker_service() -> RerankerService:
    return reranker_service
