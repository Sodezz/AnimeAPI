from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Инициализировать логирование
import utils.loguru_config  # noqa: F401

from schemas.anime_response import Anime
from services.fetch_anime_service import search_anime, search_popular_anime

app = FastAPI(title="AnimeAPI", description="Поиск и получение информации об аниме", version="1.0.0")

# CORS (при необходимости настройте origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
async def read_root():
    return {"hello": "world"}


@app.get(
    "/anime/popular",
    response_model=list[Anime],
    summary="Получение популярных аниме",
    description="Возвращает информацию об популярных аниме.",
    tags=["anime"],
)
async def get_anime_popular(
    page: int = Query(1, ge=1, description="Номер страницы пагинации"),
    per_page: int = Query(5, ge=1, le=25, description="Количество выводимых популярных тайтлов"),
):
    search_result = await search_popular_anime(page, per_page)
    return search_result


@app.get(
    "/anime",
    response_model=list[Anime],
    summary="Получение конкретного аниме и его сиквелов",
    description="Возвращает информацию о аниме.",
    tags=["anime"],
)
async def get_anime(
    page: int = Query(1, ge=1, description="Номер страницы пагинации"),
    per_page: int = Query(5, ge=1, le=25, description="Количество выводимых тайтлов"),
    search: str | None = Query(None, description="Строка поиска по названию аниме"),
):
    search_result = await search_anime(page, per_page, search)
    return search_result
