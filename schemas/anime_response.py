from pydantic import BaseModel, Field


class Anime(BaseModel):
    russian_anime_title: str = Field(..., examples=["Атака Титанов"])
    average_score_anime: int = Field(..., examples=[85])
