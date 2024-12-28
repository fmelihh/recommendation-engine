from pydantic import BaseModel, Field


class SearchDto(BaseModel):
    page: int = Field(default=0)
    page_size: int = Field(default=10)
    search_text: str
    lat: float | None = Field(default=None)
    lon: float | None = Field(default=None)
