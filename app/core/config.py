from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    upload_dir: Path = Field(default=Path("storage/uploads"))
    metadata_dir: Path = Field(default=Path("storage/metadata"))
    chroma_dir: Path = Field(default=Path("storage/chroma"))

    chunk_size: int = Field(default=1000, ge=100)
    chunk_overlap: int = Field(default=200, ge=0)

    embedding_model: str = Field(default="all-MiniLM-L6-v2")
    llm_model: str = Field(default="llama3.2")

    log_level: str = Field(default="INFO")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()