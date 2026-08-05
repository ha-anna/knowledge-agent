import logging

import chromadb

from app.core.config import settings
from app.core.services import embedding_service
from app.domain.chunk import EmbeddedChunk
from app.domain.search import SearchResult

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self) -> None:
        logger.info("Initializing vector store")

        self.client = chromadb.PersistentClient(
            path=str(settings.vector_db_dir)
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

        logger.info("Vector store ready")

    def add(
        self,
        chunks: list[EmbeddedChunk],
    ) -> None:
        if not chunks:
            logger.info("No embedded chunks to add.")
            return

        ids = [ec.source_chunk.id for ec in chunks]
        documents = [ec.source_chunk.text for ec in chunks]
        embeddings = [ec.embedding for ec in chunks]
        metadatas = [{
            "document_id": ec.source_chunk.id,
            "chunk_index": ec.source_chunk.index,
        } for ec in chunks]

        logger.info("Adding %d chunks to vector store", len(ids))

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        logger.info("Successfully stored %d chunks", len(ids))

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:

        query_embedding = embedding_service.embed_text(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        return results






