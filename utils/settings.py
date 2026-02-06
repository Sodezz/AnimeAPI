from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    anilist_url: str = Field(default="https://graphql.anilist.co")
    shikimori_url: str = Field(default="https://shikimori.one/api/graphql")
    request_timeout_seconds: float = Field(default=15.0, ge=1.0, le=60.0)
    max_retries: int = Field(default=3, ge=1, le=10)
    translation_cache_ttl_seconds: int = Field(default=21_600, ge=60)
    user_agent: str = Field(default="AnimeAPI/2.0")
    auth_shikimori: str | None = Field(default=None)
    log_level: str = Field(default="INFO")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
