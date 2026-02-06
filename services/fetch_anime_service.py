from __future__ import annotations

import requests
from loguru import logger

from services.translate_service import translate_titles
from utils.get_data_json import get_title

ANILIST_URL = "https://graphql.anilist.co"
ANILIST_TIMEOUT_SECONDS = 15
ANILIST_QUERY_SEARCH = """
query($page: Int, $perPage: Int, $search: String)  {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: POPULARITY_DESC, search: $search) {
      id
      averageScore
      title {
        english
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
      }
    }
  }
}
"""


def _post_anilist(query: str, variables: dict) -> dict:
    logger.debug("Отправка запроса в AniList GraphQL")
    response = requests.post(
        ANILIST_URL,
        json={"query": query, "variables": variables},
        timeout=ANILIST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def search_current_anime(page: int, per_page: int, search: str | None) -> list[dict]:
    """
    Выполняет поиск аниме по названию через API AniList и возвращает переведённые названия с оценками.

    Args:
        page (int): Номер страницы.
        per_page (int): Количество элементов на странице.
        search (str): Поисковый запрос (английское название).

    Returns:
        list[dict]: Список переведённых тайтлов с их оценками.
    """
    logger.debug("Поиск аниме по запросу: %s", search)
    variables = {"page": page, "perPage": per_page, "search": search}
    data = _post_anilist(ANILIST_QUERY_SEARCH, variables)
    result = get_title(data)
    logger.debug("Перевод тайтлов после поиска")
    return translate_titles(result)


def search_popular_anime(page: int, per_page: int) -> list[dict]:
    """
    Получает популярные аниме с API AniList и возвращает переведённые названия с оценками.

    Args:
        page (int): Номер страницы.
        per_page (int): Количество элементов на странице.

    Returns:
        list[dict]: Список переведённых популярных тайтлов с оценками.
    """
    variables = {"page": page, "perPage": per_page}
    data = _post_anilist(ANILIST_QUERY_POPULAR, variables)
    result = get_title(data)
    return translate_titles(result)
