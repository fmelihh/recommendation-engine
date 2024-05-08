from dataclasses import dataclass
from ...mixins import DataclassValidationMixin


@dataclass(frozen=True)
class CommentValue(DataclassValidationMixin):
    review_id: str
    date_text: str
    restaurant_rating: int
    restaurant_comment: str
    restaurant_reply: str | None
    chips_rating: list[str] | None

    def validate_review_id(self) -> str:
        if not isinstance(self.review_id, str):
            raise ValueError("Invalid id type expected.")
        return self.review_id

    def validate_date_text(self) -> str:
        if not isinstance(self.date_text, str):
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

    def validate_chips_rating(self) -> list[str] | None:
        if self.chips_rating and not isinstance(self.chips_rating, list):
            raise ValueError("Invalid comment chips rating type expected.")
        if not self.chips_rating:
            return None

        return [
            element.get("chipText")
            for element in self.chips_rating
            if isinstance(element, dict) and element.get("chipText")
        ]
