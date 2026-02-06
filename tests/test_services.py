from __future__ import annotations

import httpx
import pytest

from services.fetch_anime_service import ANILIST_QUERY_POPULAR, AniListService
from services.translate_service import SHIKIMORI_QUERY, ShikimoriTranslator
from utils.settings import Settings


@pytest.mark.asyncio
async def test_anilist_service_fetch_popular() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == httpx.URL("https://graphql.anilist.co")
        payload = request.read().decode()
        assert ANILIST_QUERY_POPULAR.strip()[:20] in payload
        return httpx.Response(
            200,
            json={
                "data": {
                    "Page": {
                        "media": [
                            {
                                "id": 1,
                                "averageScore": 90,
                                "title": {"english": "One Piece", "romaji": "One Piece"},
                            }
                        ]
                    }
                }
            },
        )

    transport = httpx.MockTransport(handler)
    settings = Settings()

    async with httpx.AsyncClient(transport=transport) as client:
        service = AniListService(client, settings)
        result = await service.fetch_popular(page=1, per_page=1)

    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].english_title == "One Piece"
    assert result[0].average_score == 90


@pytest.mark.asyncio
async def test_shikimori_translator_cache() -> None:
    counter = {"calls": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        counter["calls"] += 1
        payload = request.read().decode()
        assert SHIKIMORI_QUERY.strip()[:20] in payload
        return httpx.Response(200, json={"data": {"animes": [{"russian": "Наруто"}]}})

    transport = httpx.MockTransport(handler)
    settings = Settings(translation_cache_ttl_seconds=60)

    async with httpx.AsyncClient(transport=transport) as client:
        translator = ShikimoriTranslator(client, settings)
        first = await translator.translate_title("Naruto")
        second = await translator.translate_title("naruto")

    assert first == "Наруто"
    assert second == "Наруто"
    assert counter["calls"] == 1
