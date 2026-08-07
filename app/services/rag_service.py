import logging

from app.domain.rag import RAGResponse
from app.prompts.rag_prompt import build_context, build_rag_messages
from app.services.llm.ollama_service import OllamaService
from app.services.reranker_service import RerankerService
from app.services.vector_store import VectorStore

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(
        self,
        vector_store: VectorStore,
        llm_service: OllamaService,
        reranker_service: RerankerService,
    ):
        self.vector_store = vector_store
        self.llm_service = llm_service
        self.reranker_service = reranker_service
    
    def answer(self, question: str) -> RAGResponse:
        logger.info("Searching vector store")

        results = self.vector_store.search(question)

        for result in results:
            logger.info(
                "Retrieved page=%s distance=%s text=%s",
                result.page_number,
                result.distance,
                result.text[:100],
            )

        logger.info("Retrieved %d chunks", len(results))

        results = self.reranker_service.rerank(
            question,
            results,
            top_k=5,
        )
        
        context = build_context(results)

        logger.info("Building prompt")

        messages = build_rag_messages(
            question=question,
            context=context,
        )

        logger.info("Generating answer")

        answer = self.llm_service.generate(messages)

        return RAGResponse(
            answer=answer,
            sources=[
                result.to_source()
                for result in results
            ],
        )
    