from pydantic import BaseModel, Field


class Anime(BaseModel):
    russian_title: str = Field(..., examples=["Атака Титанов"], description="Русское название аниме")
    average_score: int | None = Field(
        ..., examples=[85], description="Средняя оценка аниме (может отсутствовать)"
    )
