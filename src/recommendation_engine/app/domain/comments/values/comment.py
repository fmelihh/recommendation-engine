from dataclasses import dataclass
from ...mixins import DataclassValidationMixin


@dataclass(frozen=True)
class CommentValue(DataclassValidationMixin):
    review_id: str
    date_text: str
    restaurant_reply: str
    restaurant_rating: int
    restaurant_comment: str
