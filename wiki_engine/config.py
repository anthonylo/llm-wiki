from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")

    wiki_dir: Path = Field(default=Path("wiki"), alias="WIKI_DIR")
    inbox_dir: Path = Field(default=Path("inbox"), alias="INBOX_DIR")
    store_dir: Path = Field(default=Path(".wiki_store"), alias="STORE_DIR")

    generation_model: str = Field(default="claude-opus-4-6", alias="GENERATION_MODEL")
    validation_model: str = Field(default="claude-opus-4-6", alias="VALIDATION_MODEL")
    linking_model: str = Field(default="claude-haiku-4-5-20251001", alias="LINKING_MODEL")

    max_rows_per_prompt: int = Field(default=200, alias="MAX_ROWS_PER_PROMPT")

    @property
    def chroma_dir(self) -> Path:
        return self.store_dir / "chroma"

    @property
    def processed_dir(self) -> Path:
        return self.store_dir / "processed"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
