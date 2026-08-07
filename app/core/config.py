from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    upload_dir: Path = Field(default=Path("storage/uploads"))
    metadata_dir: Path = Field(default=Path("storage/metadata"))
    vector_db_dir: Path = Path("storage/vectors")

    chunk_size: int = Field(default=1000, ge=100)
    chunk_overlap: int = Field(default=200, ge=0)

    embedding_model: str = Field(default="all-MiniLM-L6-v2")
    ollama_model: str = Field(default="llama3.2:3b")

    ollama_base_url: str = Field(default="http://ollama:11434")

    log_level: str = Field(default="INFO")
    top_k: int = Field(default=5, ge=1)
    distance_threshold: float = 0.75

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()