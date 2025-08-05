from fastapi import FastAPI, Query

from schemas.anime_response import Anime
from services.fetch_anime_service import search_current_anime, search_popular_anime

app = FastAPI()


@app.get("/")
async def read_root():
    return {"hello": "world"}


@app.get(
    "/anime/popular",
    response_model=list[Anime],
    summary="Получение популярных аниме",
    description="Возвращает информацию об популярных аниме.",
)
def get_anime_popular(
    page: int = Query(1, description="Номер страницы пагинации"),
    per_page: int = Query(5, description="Количество выводимых популярных тайтлов"),
):
    search_result = search_popular_anime(page, per_page)
    return search_result


@app.get(
    "/anime/",
    response_model=list[Anime],
    summary="Получение конкретного аниме и его сиквелов",
    description="Возвращает информацию о аниме.",
)
def get_anime(
    page: int = Query(1, description="Номер страницы пагинации"),
    per_page: int = Query(5, description="Количество выводимых тайтлов"),
    search: str = Query(None, description="Строка поиска по названию аниме"),
):
    search_result = search_current_anime(page, per_page, search)
    return search_result
