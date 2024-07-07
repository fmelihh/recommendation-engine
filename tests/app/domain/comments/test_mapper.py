import datetime

from src.recommendation_engine.app.features.comments.dto.comment import CommentDto
from src.recommendation_engine.app.features.comments.mappers.comment import (
    CommentMapper,
)
from src.recommendation_engine.app.features.comments.domain.values.getir import (
    GetirCommentValue,
)
from src.recommendation_engine.app.features.comments.domain.values.yemeksepeti.comment import (
    YemeksepetiCommentValue,
    YemeksepetiReplies,
    YemekSepetiRating,
    ProductVariation,
)


def test_getir_mapper():
    getir_domain_value = GetirCommentValue(
        review_id="test",
        date_text="test",
        restaurant_rating=2,
        restaurant_comment="a",
        restaurant_reply="a",
    )
    res = CommentMapper.getir_comment_to_dto(value_object=getir_domain_value)
    assert isinstance(res, CommentDto)


def test_yemeksepeti_mapper():
    yemeksepeti_domain_value = YemeksepetiCommentValue(
        comment_id="test",
        created_at="2023-07-07T23:00:00",
        comment="test",
        reviewer_name="test",
        reviewer_id="test",
        rating=[
            {"topic": "overall", "score": 1},
            {"topic": "restaurant_food", "score": 1},
            {"topic": "rider", "score": 1}
        ],
        comment_like_count=2,
        product_variation=[],
        replies=[
            {
                "id": "test",
                "text": "text",
                "createdAt": "2023-07-07T23:00:00",
                "updatedAt": "2023-07-07T23:00:00",
            },
            {
                "id": "test",
                "text": "text",
                "createdAt": "2023-07-07T23:00:00",
                "updatedAt": "2023-07-07T23:00:00",
            },
            {
                "id": "test",
                "text": "text",
                "createdAt": "2023-07-07T23:00:00",
                "updatedAt": "2023-07-07T23:00:00",
            },
        ],
        updated_at="2023-07-07T23:00:00",
    )

    res = CommentMapper.yemeksepeti_comment_to_dto(
        value_object=yemeksepeti_domain_value
    )
    assert isinstance(res, CommentDto)
