from __future__ import annotations

from typing import Any

import httpx

from schemas.anime_response import Anime
from services.exceptions import ExternalServiceError
from utils.loguru_config import get_logger
from utils.settings import Settings

logger = get_logger(__name__)

ANILIST_QUERY_SEARCH = """
query($page: Int, $perPage: Int, $search: String)  {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: POPULARITY_DESC, search: $search) {
      id
      averageScore
      title {
        english
        romaji
      }
    }
  }
}
"""

ANILIST_QUERY_POPULAR = """
query($page: Int, $perPage: Int)  {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: POPULARITY_DESC) {
      id
      averageScore
      title {
        english
        romaji
      }
    }
  }
}
"""


class AniListService:
    def __init__(self, client: httpx.AsyncClient, settings: Settings) -> None:
        self._client = client
        self._settings = settings

    async def fetch_popular(self, page: int, per_page: int) -> list[Anime]:
        data = await self._post_graphql(ANILIST_QUERY_POPULAR, {"page": page, "perPage": per_page})
        return self._extract_anime(data)

    async def fetch_by_search(self, page: int, per_page: int, search: str | None) -> list[Anime]:
        data = await self._post_graphql(
            ANILIST_QUERY_SEARCH,
            {"page": page, "perPage": per_page, "search": search},
        )
        return self._extract_anime(data)

    async def _post_graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        payload = {"query": query, "variables": variables}
        last_error: Exception | None = None

        for attempt in range(1, self._settings.max_retries + 1):
            try:
                response = await self._client.post(self._settings.anilist_url, json=payload)
                response.raise_for_status()
                body = response.json()

                if body.get("errors"):
                    raise ExternalServiceError(f"AniList GraphQL error: {body['errors']}")

                return body
            except (httpx.HTTPError, ValueError, ExternalServiceError) as error:
                last_error = error
                logger.warning("AniList request failed on attempt %s: %s", attempt, error)

        raise ExternalServiceError("AniList is unavailable") from last_error

    @staticmethod
    def _extract_anime(data: dict[str, Any]) -> list[Anime]:
        media_items = data.get("data", {}).get("Page", {}).get("media", [])
        result: list[Anime] = []

        for anime in media_items:
            title = anime.get("title") or {}
            english_title = title.get("english") or title.get("romaji")
            result.append(
                Anime(
                    id=anime.get("id"),
                    english_title=english_title,
                    russian_title=None,
                    average_score=anime.get("averageScore"),
                )
            )
        return result
