import requests
from utils.get_data_json import get_title
from services.translate_service import translate_titles
from loguru import logger

url = "https://graphql.anilist.co"


def search_current_anime(page: int, per_page: int, search: str):
    logger.debug(f"Отправка запроса в AniList GraphQL с тайтлом: {search}")
    query = """
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

    variables = {"page": page, "perPage": per_page, "search": search}

    response = requests.post(url, json={"query": query, "variables": variables})

    data = response.json()

    result = get_title(data)
    logger.debug("Перевод тайтла")
    rus_result = translate_titles(result)
    return rus_result


def search_popular_anime(page: int, per_page: int):
    query = """
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

    variables = {"page": page, "perPage": per_page}

    response = requests.post(url, json={"query": query, "variables": variables})

    data = response.json()

    result = get_title(data)
    rus_result = translate_titles(result)
    return rus_result
