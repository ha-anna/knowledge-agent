import logging

from app.domain.rag import RAGResponse
from app.prompts.rag_prompt import build_context, build_rag_messages
from app.services.llm.ollama_service import OllamaService
from app.services.vector_store import VectorStore

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(
        self,
        vector_store: VectorStore,
        llm_service: OllamaService,
    ):
        self.vector_store = vector_store
        self.llm_service = llm_service
    
    def answer(self, question: str) -> RAGResponse:
        logger.info("Searching vector store")

        results = self.vector_store.search(question)

        logger.info("Retrieved %d chunks", len(results))
        
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
            sources=results,
        )
    