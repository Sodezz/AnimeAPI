from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query, Request
import httpx

from schemas.anime_response import Anime
from services.catalog_service import AnimeCatalogService
from services.fetch_anime_service import AniListService
from services.translate_service import ShikimoriTranslator
from utils.loguru_config import configure_logging, get_logger
from utils.settings import get_settings

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings.log_level)

    app.state.anilist_client = httpx.AsyncClient(
        timeout=settings.request_timeout_seconds,
        headers={"User-Agent": settings.user_agent},
    )
    app.state.shikimori_client = httpx.AsyncClient(
        timeout=settings.request_timeout_seconds,
        headers={"User-Agent": settings.user_agent},
    )

    anilist_service = AniListService(app.state.anilist_client, settings)
    translator = ShikimoriTranslator(app.state.shikimori_client, settings)
    app.state.catalog_service = AnimeCatalogService(anilist_service, translator)

    logger.info("AnimeAPI started")
    try:
        yield
    finally:
        await app.state.anilist_client.aclose()
        await app.state.shikimori_client.aclose()
        logger.info("AnimeAPI stopped")


app = FastAPI(
    title="AnimeAPI",
    version="2.0.0",
    description="Production-ready API for anime discovery with Russian title enrichment.",
    lifespan=lifespan,
)


def get_catalog_service(request: Request) -> AnimeCatalogService:
    return request.app.state.catalog_service


@app.get("/", summary="Health check")
async def read_root() -> dict[str, str]:
    return {"status": "ok", "service": "anime-api"}


@app.get("/anime/popular", response_model=list[Anime], summary="Get popular anime")
async def get_anime_popular(
    page: int = Query(1, ge=1, description="Pagination page number"),
    per_page: int = Query(10, ge=1, le=50, description="Items per page"),
    service: AnimeCatalogService = Depends(get_catalog_service),
) -> list[Anime]:
    return await service.get_popular(page=page, per_page=per_page)


@app.get("/anime", response_model=list[Anime], summary="Search anime")
async def get_anime(
    page: int = Query(1, ge=1, description="Pagination page number"),
    per_page: int = Query(10, ge=1, le=50, description="Items per page"),
    search: str | None = Query(None, min_length=1, description="Anime title query"),
    service: AnimeCatalogService = Depends(get_catalog_service),
) -> list[Anime]:
    return await service.search(page=page, per_page=per_page, search=search)
