from app.core.dependencies.embedding import embedding_service
from app.services.vector_store import VectorStore

vector_store = VectorStore(embedding_service)