import datetime
from pydantic import HttpUrl
from dataclasses import dataclass

from ..comment import CommentValue
from .rating import YemekSepetiRating
from .replies import YemeksepetiReplies
from .product_variation import ProductVariation


@dataclass(frozen=True)
class YemeksepetiCommentValue(CommentValue):
    comment_id: str | None
    created_at: datetime.datetime | str | None
    updated_at: datetime.datetime | str | None
    comment: str | None
    reviewer_name: str | None
    reviewer_id: str | None
    rating: YemekSepetiRating | list[dict] | None
    comment_like_count: int | None
    product_variation: list[ProductVariation] | list[dict] | None
    replies: list[YemeksepetiReplies] | list[dict] | None
