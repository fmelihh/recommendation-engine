from typing import TypeVar

from ..dto.comment import CommentDto
from ..domain.values.getir import GetirCommentValue
from ..domain.values.yemeksepeti import YemeksepetiCommentValue


CommentValue = TypeVar("CommentValue", GetirCommentValue, YemeksepetiCommentValue)


class CommentMapper:
    @staticmethod
    def yemeksepeti_comment_to_dto(value_object: YemeksepetiCommentValue) -> CommentDto:
        pass

    @staticmethod
    def getir_comment_to_dto(value_object: GetirCommentValue) -> CommentDto:
        # TODO: getir comment value date text to be uptaded.
        comment_dto = CommentDto(
            reply=value_object.restaurant_reply,
            rating=value_object.restaurant_rating,
            comment=value_object.restaurant_comment,
            comment_id=value_object.review_id,
        )
        return comment_dto
