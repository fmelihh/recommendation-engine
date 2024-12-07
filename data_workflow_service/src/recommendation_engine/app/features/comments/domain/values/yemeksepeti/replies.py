import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class YemeksepetiReplies:
    reply_id: str
    text: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
