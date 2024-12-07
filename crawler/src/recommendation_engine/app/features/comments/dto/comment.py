import datetime
from pydantic import BaseModel, Field


class CommentDto(BaseModel):
    rating: int
    comment: str
    comment_id: str
    replies: list[str]
    like_count: int = Field(default=0)
    created_at: datetime.datetime | None = Field(default=None)
    updated_at: datetime.datetime | None = Field(default=None)
