import logging
from functools import cached_property

from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.domain.chunk import Chunk, EmbeddedChunk

logger = logging.getLogger(__name__)


class EmbeddingService:
    @cached_property
    def model(self) -> SentenceTransformer:
        logger.info("Loading embedding model '%s'...", settings.embedding_model)
        model = SentenceTransformer(settings.embedding_model)
        logger.info("Embedding model loaded.")
        return model

    def embed_chunk(self, chunk: Chunk) -> EmbeddedChunk:
        embedding = self.model.encode(
            chunk.text,
            normalize_embeddings=True,
        )

        return EmbeddedChunk(
            source_chunk=chunk,
            embedding=embedding.tolist(),
        )

    def embed_chunks(
        self,
        chunks: list[Chunk],
    ) -> list[EmbeddedChunk]:
        if not chunks:
            return []

        logger.info("Generating embeddings for %d chunks", len(chunks))

        embeddings = self.model.encode(
            [chunk.text for chunk in chunks],
            normalize_embeddings=True,
        )

        embedded_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            embedded_chunks.append(
                EmbeddedChunk(
                    source_chunk=chunk,
                    embedding=embedding.tolist(),
                )
            )

        logger.info(
            "Generated %d embeddings",
            len(embedded_chunks),
        )

        return embedded_chunks

    def embed_text(
        self,
        text: str,
    ) -> list[float]:

        return self.model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()
