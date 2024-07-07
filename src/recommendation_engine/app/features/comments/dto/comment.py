import datetime
from pydantic import BaseModel, Field


class CommentDto(BaseModel):
    reply: str
    rating: int
    comment: str
    comment_id: str
    comment_date: datetime.datetime | None = Field(default=None)
