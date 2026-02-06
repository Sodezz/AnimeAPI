from __future__ import annotations

import os

import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

SHIKIMORI_URL = "https://shikimori.one/api/graphql"
SHIKIMORI_TIMEOUT_SECONDS = 15


def _post_shikimori(query: dict) -> dict:
    headers = {
        "Content-Type": "application/json",
    }
    user_agent = os.getenv("USERAGENT")
    authorization = os.getenv("AUTHSHIKIMORI")
    if user_agent:
        headers["User-Agent"] = user_agent
    if authorization:
        headers["Authorization"] = authorization

    response = requests.post(
        SHIKIMORI_URL,
        json=query,
        headers=headers,
        timeout=SHIKIMORI_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def translate_title(search: str) -> str | None:
    """
    Переводит английский тайтл на русский через API Shikimori.

    Args:
        search: английское название аниме.

    Returns:
        Русское название или None при ошибке.
    """
    query = {
        "query": """
        query ($search: String!) {
            animes(search: $search, limit: 1, kind: "!special") {
                russian
            }
        }
        """,
        "variables": {"search": search},
    }

    data = _post_shikimori(query)
    rus_titles = data.get("data", {}).get("animes") or []
    if not rus_titles:
        logger.warning("Не найден русский тайтл для запроса: %s", search)
        return None
    return rus_titles[0].get("russian")


def translate_titles(titles: list[dict]) -> list[dict]:
    """
    Переводит список тайтлов с английского на русский, сохраняя оценки.

    Args:
        titles (list[dict]): Список словарей с ключами 'eng_title' и 'score'.

    Returns:
        list[dict]: Список словарей с ключами 'russian_title' и 'average_score'.
    """
    logger.debug("Перевод тайтлов из списка с английского на русский")
    result: list[dict] = []
    for item in titles:
        eng_title = item.get("eng_title")
        score = item.get("score")

        if eng_title:
            rus_title = translate_title(eng_title)
            logger.debug(f"Перевод тайтла: {rus_title}")
        else:
            rus_title = None

        result.append({"russian_anime_title": rus_title, "average_score_anime": score})

    return result
