from typing import TypeVar

from ..dto.comment import CommentDto
from ..domain.values.getir import GetirCommentValue
from ..domain.values.yemeksepeti import YemeksepetiCommentValue


CommentValue = TypeVar("CommentValue", GetirCommentValue, YemeksepetiCommentValue)


class CommentMapper:
    @staticmethod
    def yemeksepeti_comment_to_dto(value_object: YemeksepetiCommentValue) -> CommentDto:
        # TODO: product variation field must be handle.

        comment_dto = CommentDto(
            rating=value_object.rating.overall_rating,
            comment=value_object.comment,
            comment_id=value_object.comment_id,
            replies=[reply.text for reply in value_object.replies],
            like_count=value_object.comment_like_count,
            created_at=value_object.created_at,
            updated_at=value_object.updated_at,
        )
        return comment_dto

    @staticmethod
    def getir_comment_to_dto(value_object: GetirCommentValue) -> CommentDto:
        # TODO: getir comment value date text to be updated.
        comment_dto = CommentDto(
            replies=(
                []
                if value_object.restaurant_reply is None
                else [value_object.restaurant_reply]
            ),
            rating=value_object.restaurant_rating,
            comment=value_object.restaurant_comment,
            comment_id=value_object.review_id,
        )
        return comment_dto
