import pendulum
import datetime
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

    def validate_comment_id(self) -> str | None:
        if not isinstance(self.comment_id, str):
            raise ValueError("Invalid id type expected.")
        return self.comment_id

    def validate_created_at(self) -> datetime.datetime | None:
        if not isinstance(self.created_at, str):
            raise ValueError("Invalid created_at type expected.")

        pendulum_date = pendulum.from_format(self.created_at.replace("Z", ""), "YYYY-MM-DDTHH:mm:ss")
        return datetime.datetime(
            year=pendulum_date.year,
            month=pendulum_date.month,
            day=pendulum_date.day,
            hour=pendulum_date.hour,
            minute=pendulum_date.minute,
            second=pendulum_date.second,
        )

    def validate_updated_at(self) -> datetime.datetime | None:
        if not isinstance(self.updated_at, str):
            raise ValueError("Invalid created_at type expected.")

        pendulum_date = pendulum.from_format(self.updated_at.replace("Z", ""), "YYYY-MM-DDTHH:mm:ss")
        return datetime.datetime(
            year=pendulum_date.year,
            month=pendulum_date.month,
            day=pendulum_date.day,
            hour=pendulum_date.hour,
            minute=pendulum_date.minute,
            second=pendulum_date.second,
        )

    def validate_comment(self) -> str:
        if not isinstance(self.comment, str):
            raise ValueError("Invalid comment type expected.")
        return self.comment

    def validate_reviewer_name(self) -> str:
        if not isinstance(self.reviewer_name, str):
            raise ValueError("Invalid reviewer name type expected.")
        return self.reviewer_name

    def validate_reviewer_id(self) -> str:
        if not isinstance(self.reviewer_id, str):
            raise ValueError("Invalid reviewer id type expected.")
        return self.reviewer_id

    def validate_rating(self) -> YemekSepetiRating:
        if not isinstance(self.rating, list):
            raise ValueError("Invalid rating type expected.")
        values = {
            "overall_rating": None,
            "restaurant_rating": None,
            "rider_rating": None,
        }
        for rate in self.rating:
            topic = rate.get("topic")
            score = rate.get("score", 0)

            if topic == "overall":
                values["overall_rating"] = score
            elif topic == "restaurant_food":
                values["restaurant_rating"] = score
            elif topic == "rider":
                values["rider_rating"] = score

        return YemekSepetiRating(**values)

    def validate_comment_like_count(self) -> int:
        if not isinstance(self.comment_like_count, int):
            raise ValueError("Invalid comment_like_count type expected.")
        return self.comment_like_count

    def validate_product_variation(self) -> list[ProductVariation] | None:
        if not isinstance(self.product_variation, list):
            raise ValueError("Invalid product_variation type expected.")

        product_variation_list = []
        for product_variation in self.product_variation:
            product_variation_list.append(
                ProductVariation(
                    product_variation_id=product_variation.get("id"),
                    title=product_variation.get("defaultTitle"),
                    unit_price=product_variation.get("unitPrice", 0),
                    description=product_variation.get("product", {}).get("description"),
                    image_urls=product_variation.get("product", {}).get(
                        "imageUrls", []
                    ),
                )
            )

        return product_variation_list

    def validate_replies(self) -> list[YemeksepetiReplies] | None:
        if not isinstance(self.replies, list):
            raise ValueError("Invalid replies type expected.")

        replies_list = []
        for reply in self.replies:
            created_at = pendulum.from_format(
                reply["createdAt"].replace("Z", ""), "YYYY-MM-DDTHH:mm:ss"
            )
            updated_at = pendulum.from_format(
                reply["updatedAt"].replace("Z", ""), "YYYY-MM-DDTHH:mm:ss"
            )
            created_at = datetime.datetime(
                year=created_at.year,
                month=created_at.month,
                day=created_at.day,
                hour=created_at.hour,
                minute=created_at.minute,
                second=created_at.second,
            )
            updated_at = datetime.datetime(
                year=updated_at.year,
                month=updated_at.month,
                day=updated_at.day,
                hour=updated_at.hour,
                minute=updated_at.minute,
                second=updated_at.second,
            )

            replies_list.append(
                YemeksepetiReplies(
                    reply_id=reply.get("id"),
                    text=reply.get("text"),
                    created_at=created_at,
                    updated_at=updated_at,
                )
            )

        return replies_list
