from src.recommendation_engine.app.features.comments.domain.entity.yemek_sepeti import (
    YemekSepetiComments,
)
from src.recommendation_engine.app.features.comments.dto.comment import (
    CommentDto,
)


def test_yemeksepeti_comments():
    yemek_sepeti_comments = YemekSepetiComments(restaurant_id="nrp4")
    results = yemek_sepeti_comments.process(process_limit=1)
    assert isinstance(results, list)
    assert len(results) > 0


def test_getir_comments_with_dto():
    yemek_sepeti_comments = YemekSepetiComments(restaurant_id="nrp4")
    results = yemek_sepeti_comments.process(process_limit=1)
    [
        CommentDto(
            rating=value_object.rating.overall_rating,
            comment=value_object.comment,
            comment_id=value_object.comment_id,
            replies=[reply.text for reply in value_object.replies],
            like_count=value_object.comment_like_count,
            created_at=value_object.created_at,
            updated_at=value_object.updated_at,
        )
        for value_object in results
    ]
    assert isinstance(results, list)
    assert len(results) > 0
