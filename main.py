from fastapi import FastAPI

from services.fetch_anime_service import search_current_anime, search_popular_anime

app = FastAPI()


@app.get("/")
async def read_root():
    return {"hello": "world"}


@app.get("/anime/popular")
def get_anime_popular(page: int = 1, per_page: int = 5):
    search_result = search_popular_anime(page, per_page)
    return search_result


@app.get("/anime/")
def get_anime(page: int = 1, per_page: int = 5, search: str = "None"):
    search_result = search_current_anime(page, per_page, search)
    return search_result
