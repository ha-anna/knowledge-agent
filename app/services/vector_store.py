import logging

import chromadb

from app.core.config import settings
from app.domain.chunk import EmbeddedChunk
from app.domain.search import SearchResult
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self, embedding_service: EmbeddingService,) -> None:
        self.embedding_service = embedding_service

        logger.info("Initializing vector store")
        

        self.client = chromadb.PersistentClient(
            path=str(settings.vector_db_dir)
        )

        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={
                "hnsw:space": "cosine"
            }
        )

        logger.info("Vector store ready")

    def add(
        self,
        chunks: list[EmbeddedChunk],
    ) -> None:
        if not chunks:
            logger.info("No embedded chunks to add.")
            return


        #temporary
        for ec in chunks:
            logger.info(
                "ADDING | page=%s chunk=%s text=%s",
                ec.source_chunk.page_number,
                ec.source_chunk.index,
                ec.source_chunk.text[:200],
            )

        ids = [ec.source_chunk.id for ec in chunks]
        documents = [ec.source_chunk.text for ec in chunks]
        embeddings = [ec.embedding for ec in chunks]
        metadatas = [
            {
                "document_id": ec.source_chunk.document_id,
                "filename": ec.source_chunk.filename,
                "page_number": ec.source_chunk.page_number,
                "chunk_index": ec.source_chunk.index,
            }
            for ec in chunks
        ]

        logger.info("Adding %d chunks to vector store", len(ids))

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        logger.info("Successfully stored %d chunks", len(ids))

    def search(
        self,
        query: str,
        top_k_retrieval: int = settings.top_k_retrieval,
    ) -> list[SearchResult]:

        embedding = self.embedding_service.embed_text(query)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k_retrieval,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        search_results = []

        for i in range(len(results["ids"][0])):

            distance = results["distances"][0][i]

            if distance > settings.distance_threshold:
                continue

            search_results.append(
                SearchResult(
                    document_id=results["metadatas"][0][i]["document_id"],
                    chunk_id=results["ids"][0][i],
                    filename=results["metadatas"][0][i]["filename"],
                    page_number=results["metadatas"][0][i]["page_number"],
                    text=results["documents"][0][i],
                    distance=distance,
                )
            )

        return search_results

    def delete_document(self, document_id: str):

        self.collection.delete(
            where={
                "document_id": document_id
            }
        )
    






