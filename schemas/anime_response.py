from pydantic import BaseModel, Field


class Anime(BaseModel):
    id: int = Field(..., examples=[16498], description="AniList anime ID")
    english_title: str | None = Field(None, examples=["Attack on Titan"], description="English title")
    russian_title: str | None = Field(None, examples=["Атака титанов"], description="Russian localized title")
    average_score: int | None = Field(None, examples=[84], description="Average AniList score")
