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






