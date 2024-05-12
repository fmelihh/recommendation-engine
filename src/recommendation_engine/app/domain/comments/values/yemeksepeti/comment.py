import datetime
from pydantic import HttpUrl
from dataclasses import dataclass

from ..comment import CommentValue
from .rating import YemekSepetiRating
from .replies import YemeksepetiReplies
from .product_variation import ProductVariation


@dataclass(frozen=True)
class YemeksepetiCommentValue(CommentValue):
    comment_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    comment: str
    reviewer_name: str
    reviewer_id: str
    rating: YemekSepetiRating | list[dict] | None
    comment_like_count: int
    product_variation: list[ProductVariation] | None
    replies: list[YemeksepetiReplies] | None
