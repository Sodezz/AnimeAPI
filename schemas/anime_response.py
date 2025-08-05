from pydantic import BaseModel, Field


class Anime(BaseModel):
    russian_anime_title: str = Field(..., examples=["Атака Титанов"], description="Русское название аниме")
    average_score_anime: int = Field(..., examples=[85], description="Средняя оценка аниме")
