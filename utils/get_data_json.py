from loguru import logger


def get_title(data):
    logger.debug("Получение название тайтла")
    result = []
    for anime in data["data"]["Page"]["media"]:
        eng_title = anime["title"].get("english")
        result.append(eng_title)
    return result
