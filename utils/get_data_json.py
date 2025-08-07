from loguru import logger


def get_title(data: dict) -> list[dict]:
    """
    Извлекает названия и оценки из ответа GraphQL API AniList.

    Args:
        data (dict): JSON-ответ от API AniList.

    Returns:
        list[dict]: Список словарей с ключами 'eng_title' и 'score'.
    """
    logger.debug("Получение название тайтла")
    result = []
    media = data.get("data", {}).get("Page", {}).get("media", []) or []
    for anime in media:
        title_obj = anime.get("title") or {}
        eng_title = (
            title_obj.get("english")
            or title_obj.get("romaji")
            or title_obj.get("native")
        )
        score = anime.get("averageScore")
        result.append({"eng_title": eng_title, "score": score})
    return result
