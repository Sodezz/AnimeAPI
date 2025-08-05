import os

import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def translate_title(search: str) -> str:
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

    headers = {
        "Content-Type": "application/json",
        "User-Agent": os.getenv("USERAGENT"),
        "Authorization": os.getenv("AUTHSHIKIMORI"),
    }

    response = requests.post(
        "https://shikimori.one/api/graphql", json=query, headers=headers
    )

    data = response.json()
    rus_titles = data.get("data").get("animes")

    return rus_titles[0]["russian"]


def translate_titles(titles) -> list[dict]:
    """
    Переводит список тайтлов с английского на русский, сохраняя оценки.

    Args:
        titles (list[dict]): Список словарей с ключами 'eng_title' и 'score'.

    Returns:
        list[dict]: Список словарей с ключами 'russian_title' и 'average_score'.
    """
    logger.debug("Перевод тайтлов из списка с английского на русский")
    result = []
    for item in titles:
        eng_title = item["eng_title"]
        score = item["score"]

        if eng_title:
            rus_title = translate_title(eng_title)
            logger.debug(f"Перевод тайтла: {rus_title}")
        else:
            rus_title = None

        result.append({"russian_anime_title": rus_title, "average_score_anime": score})

    return result
