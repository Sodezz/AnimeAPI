from __future__ import annotations

import time
from typing import Any

import httpx

from schemas.anime_response import Anime
from services.exceptions import ExternalServiceError
from utils.loguru_config import get_logger
from utils.settings import Settings

logger = get_logger(__name__)

SHIKIMORI_QUERY = """
query ($search: String!) {
  animes(search: $search, limit: 1, kind: "!special") {
    russian
  }
}
"""


class ShikimoriTranslator:
    def __init__(self, client: httpx.AsyncClient, settings: Settings) -> None:
        self._client = client
        self._settings = settings
        self._cache: dict[str, tuple[float, str | None]] = {}

    async def enrich_titles(self, titles: list[Anime]) -> list[Anime]:
        for anime in titles:
            if anime.english_title:
                anime.russian_title = await self.translate_title(anime.english_title)
        return titles

    async def translate_title(self, search: str) -> str | None:
        cached = self._cache.get(search.lower())
        if cached and cached[0] > time.monotonic():
            return cached[1]

        headers = {}
        if self._settings.auth_shikimori:
            headers["Authorization"] = self._settings.auth_shikimori

        payload = {"query": SHIKIMORI_QUERY, "variables": {"search": search}}
        last_error: Exception | None = None

        for attempt in range(1, self._settings.max_retries + 1):
            try:
                response = await self._client.post(self._settings.shikimori_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()

                if data.get("errors"):
                    raise ExternalServiceError(f"Shikimori GraphQL error: {data['errors']}")

                translated = self._extract_russian_title(data)
                self._cache[search.lower()] = (
                    time.monotonic() + self._settings.translation_cache_ttl_seconds,
                    translated,
                )
                return translated
            except (httpx.HTTPError, ValueError, ExternalServiceError) as error:
                last_error = error
                logger.warning("Shikimori request failed on attempt %s: %s", attempt, error)

        raise ExternalServiceError("Shikimori is unavailable") from last_error

    @staticmethod
    def _extract_russian_title(data: dict[str, Any]) -> str | None:
        items = data.get("data", {}).get("animes") or []
        if not items:
            return None
        return items[0].get("russian")
