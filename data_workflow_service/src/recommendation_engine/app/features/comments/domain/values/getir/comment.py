from dataclasses import dataclass
from ..comment import CommentValue


@dataclass(frozen=True)
class GetirCommentValue(CommentValue):
    review_id: str
    date_text: str
    restaurant_rating: int
    restaurant_comment: str
    restaurant_reply: str | None

    def validate_review_id(self) -> str:
        if self.review_id and not isinstance(self.review_id, str):
            raise ValueError("Invalid id type expected.")
        return self.review_id

    def validate_date_text(self) -> str:
        if self.date_text and not isinstance(self.date_text, str):
            raise ValueError("Invalid comment date text type expected.")
        return self.date_text

    def validate_restaurant_rating(self) -> int:
        if not isinstance(self.restaurant_rating, int):
            raise ValueError("Invalid comment rating type expected.")
        return self.restaurant_rating

    def validate_restaurant_reply(self) -> str | None:
        if self.restaurant_reply and not isinstance(self.restaurant_reply, str):
            raise ValueError("Invalid comment reply type expected.")
        return self.restaurant_reply

    def validate_restaurant_comment(self) -> str:
        if not isinstance(self.restaurant_comment, str):
            raise ValueError("Invalid comment type expected.")
        return self.restaurant_comment
