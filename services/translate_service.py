import os

import requests
from loguru import logger

from dotenv import load_dotenv

load_dotenv()


def translate_title(search: str):
    query = {
        "query": f"""
        {{
            animes(search: "{search}", limit: 1, kind: "!special") {{
                russian
            }}
        }}
"""
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


def translate_titles(titles):
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

        result.append({
            "Название тайтла": rus_title,
            "Средняя Оценка": score
        })

    return result
