from __future__ import annotations

from fastapi import HTTPException, status

from schemas.anime_response import Anime
from services.exceptions import ExternalServiceError
from services.fetch_anime_service import AniListService
from services.translate_service import ShikimoriTranslator


class AnimeCatalogService:
    def __init__(self, anilist: AniListService, translator: ShikimoriTranslator) -> None:
        self._anilist = anilist
        self._translator = translator

    async def get_popular(self, page: int, per_page: int) -> list[Anime]:
        try:
            anime = await self._anilist.fetch_popular(page=page, per_page=per_page)
            return await self._translator.enrich_titles(anime)
        except ExternalServiceError as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Upstream provider is temporarily unavailable",
            ) from error

    async def search(self, page: int, per_page: int, search: str | None) -> list[Anime]:
        try:
            anime = await self._anilist.fetch_by_search(page=page, per_page=per_page, search=search)
            return await self._translator.enrich_titles(anime)
        except ExternalServiceError as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Upstream provider is temporarily unavailable",
            ) from error
