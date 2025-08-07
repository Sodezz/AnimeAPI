import os
import time
import asyncio

import httpx
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Простая in-memory TTL-кэш
_TRANSLATION_CACHE: dict[str, tuple[str | None, float]] = {}
_CACHE_TTL_SECONDS = 60 * 60 * 24  # 24h
_CACHE_LOCK = asyncio.Lock()


def _get_auth_headers() -> dict[str, str]:
    user_agent = os.getenv("USERAGENT")
    token = os.getenv("AUTHSHIKIMORI")
    if not user_agent or not token:
        raise RuntimeError("Missing USERAGENT or AUTHSHIKIMORI in .env")
    return {
        "Content-Type": "application/json",
        "User-Agent": user_agent,
        "Authorization": f"Bearer {token}",
    }


async def translate_title(search: str, client: httpx.AsyncClient) -> str | None:
    """
    Переводит тайтл на русский через API Shikimori (GraphQL).

    Args:
        search: исходное название (англ/ромадзи/нативное)
        client: общий httpx AsyncClient

    Returns:
        Русское название или None, если не найдено/ошибка
    """
    if not search:
        return None

    key = search.lower().strip()
    now = time.time()

    # Кэш-хит
    async with _CACHE_LOCK:
        cached = _TRANSLATION_CACHE.get(key)
        if cached and cached[1] > now:
            return cached[0]

    payload = {
        "query": (
            """
            query ($search: String!) {
                animes(search: $search, limit: 1, kind: "!special") {
                    russian
                }
            }
            """
        ),
        "variables": {"search": search},
    }

    try:
        headers = _get_auth_headers()
        resp = await client.post(
            "https://shikimori.one/api/graphql", json=payload, headers=headers
        )
        resp.raise_for_status()
        data = resp.json()
        animes = ((data.get("data") or {}).get("animes")) or []
        russian = animes[0].get("russian") if animes else None
    except httpx.TimeoutException:
        logger.warning("Timeout from Shikimori while translating: {}", search)
        russian = None
    except httpx.HTTPError as exc:
        logger.error("HTTP error from Shikimori: {}", exc)
        russian = None
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error translating title '{}': {}", search, exc)
        russian = None

    # Записать в кэш
    async with _CACHE_LOCK:
        _TRANSLATION_CACHE[key] = (russian, now + _CACHE_TTL_SECONDS)

    return russian


async def translate_titles(titles: list[dict]) -> list[dict]:
    """
    Переводит список тайтлов, сохраняя оценки.

    Args:
        titles: [{ 'eng_title': str | None, 'score': int | None }]

    Returns:
        [{ 'russian_title': str | None, 'average_score': int | None }]
    """
    logger.debug("Перевод тайтлов из списка с английского на русский")

    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [
            translate_title(item.get("eng_title"), client) for item in titles
        ]
        translations = await asyncio.gather(*tasks, return_exceptions=False)

    result: list[dict] = []
    for item, rus_title in zip(titles, translations):
        result.append({
            "russian_title": rus_title,
            "average_score": item.get("score"),
        })

    return result
