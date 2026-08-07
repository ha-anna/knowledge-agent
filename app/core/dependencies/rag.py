from app.core.dependencies.llm import llm_service
from app.core.dependencies.reranker import reranker_service
from app.core.dependencies.vector_store import vector_store
from app.services.rag_service import RAGService

rag_service = RAGService(
    vector_store=vector_store,
    llm_service=llm_service,
    reranker_service=reranker_service,
)