import logging

from ollama import Client

from app.core.config import settings

logger = logging.getLogger(__name__)


class OllamaService:

    def __init__(self):
        self.client = Client(
            host=settings.ollama_base_url,
        )

    def generate(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        logger.info("Generating LLM response")

        try:
            response = self.client.chat(
                model=settings.ollama_model,
                messages=messages,
            )

            logger.info(
                "LLM response generated (%d characters)",
                len(response["message"]["content"]),
            )

            return response["message"]["content"]
        
        except Exception:
            logger.exception("Failed to generate LLM response")
            raise
