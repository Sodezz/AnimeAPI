import httpx
from fastapi import HTTPException
from loguru import logger

from services.translate_service import translate_titles
from utils.get_data_json import get_title

ANILIST_URL = "https://graphql.anilist.co"


async def _fetch_from_anilist(query: str, variables: dict) -> dict:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(ANILIST_URL, json={"query": query, "variables": variables})
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="AniList timeout")
    except httpx.HTTPError as exc:
        logger.error("AniList HTTP error: {}", exc)
        raise HTTPException(status_code=502, detail="AniList upstream error")


async def search_anime(page: int, per_page: int, search: str | None) -> list[dict]:
    """
    Выполняет поиск аниме по названию через API AniList и возвращает переведённые названия с оценками.
    """
    logger.debug("Отправка запроса в AniList GraphQL с тайтлом: {}", search)
    query = (
        """
        query($page: Int, $perPage: Int, $search: String)  {
          Page(page: $page, perPage: $perPage) {
            media(type: ANIME, sort: POPULARITY_DESC, search: $search) {
              id
              averageScore
              title { english romaji native }
            }
          }
        }
        """
    )

    variables = {"page": page, "perPage": per_page, "search": search}

    data = await _fetch_from_anilist(query, variables)
    titles = get_title(data)
    logger.debug("Перевод тайтла")
    rus_result = await translate_titles(titles)
    return rus_result


async def search_popular_anime(page: int, per_page: int) -> list[dict]:
    """
    Получает популярные аниме с API AniList и возвращает переведённые названия с оценками.
    """
    query = (
        """
        query($page: Int, $perPage: Int)  {
          Page(page: $page, perPage: $perPage) {
            media(type: ANIME, sort: POPULARITY_DESC) {
              id
              averageScore
              title { english romaji native }
            }
          }
        }
        """
    )

    variables = {"page": page, "perPage": per_page}

    data = await _fetch_from_anilist(query, variables)
    titles = get_title(data)
    rus_result = await translate_titles(titles)
    return rus_result
