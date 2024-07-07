from src.recommendation_engine.app.features.comments.dto.comment import CommentDto
from src.recommendation_engine.app.features.comments.mappers.comment import (
    CommentMapper,
)
from src.recommendation_engine.app.features.comments.domain.values.getir import (
    GetirCommentValue,
)
from src.recommendation_engine.app.features.comments.domain.values.yemeksepeti import (
    YemeksepetiCommentValue,
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
    pass
