from loguru import logger


def get_title(data):
    logger.debug("Получение название тайтла")
    result = []
    for anime in data["data"]["Page"]["media"]:
        eng_title = anime["title"].get("english")
        score= anime.get("averageScore")
        result.append({"eng_title": eng_title, "score": score})
    return result
