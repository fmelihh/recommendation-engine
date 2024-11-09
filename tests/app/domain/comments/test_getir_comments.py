from src.recommendation_engine.app.features.comments.domain.entity.getir import (
    GetirComments,
)
from src.recommendation_engine.app.features.comments.dto.comment import CommentDto


def test_getir_comments():
    getir_comments = GetirComments(restaurant_id="60128f1082ce14c9bc57d68a")
    results = getir_comments.process(process_limit=1)
    assert isinstance(results, list)
    assert len(results) > 0


def test_getir_comments_with_dto():
    getir_comments = GetirComments(restaurant_id="60128f1082ce14c9bc57d68a")
    results = getir_comments.process(process_limit=1)
    [
        CommentDto(
            replies=(
                []
                if value_object.restaurant_reply is None
                else [value_object.restaurant_reply]
            ),
            rating=value_object.restaurant_rating,
            comment=value_object.restaurant_comment,
            comment_id=value_object.review_id,
        )
        for value_object in results
    ]
    assert isinstance(results, list)
    assert len(results) > 0
