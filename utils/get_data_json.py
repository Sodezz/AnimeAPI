from loguru import logger


def get_title(data: dict) -> list[dict]:
    """
    Извлекает английские названия и оценки из ответа GraphQL API AniList.

    Args:
        data (dict): JSON-ответ от API AniList.

    Returns:
        list[dict]: Список словарей с ключами 'eng_title' и 'score'.
    """
    logger.debug("Получение название тайтла")
    result = []
    for anime in data["data"]["Page"]["media"]:
        eng_title = anime["title"].get("english")
        score = anime.get("averageScore")
        result.append({"eng_title": eng_title, "score": score})
    return result
