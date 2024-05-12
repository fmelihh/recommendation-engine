import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class YemeksepetiReplies:
    text: str
    like_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
