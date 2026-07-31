import logging

import chromadb

from app.core.config import settings
from app.domain.chunk import EmbeddedChunk

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
        embedded_chunks: list[EmbeddedChunk],
    ) -> None:
        if not embedded_chunks:
            logger.info("No embedded chunks to add.")
            return

        ids = [ec.chunk.id for ec in embedded_chunks]
        documents = [ec.chunk.text for ec in embedded_chunks]
        embeddings = [ec.embedding for ec in embedded_chunks]
        metdatas = [{
            "document_id": ec.chunk.id,
            "chunk_index": ec.chunk.index,
        } for ec in embedded_chunks]

        

