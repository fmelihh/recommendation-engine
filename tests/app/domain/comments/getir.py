from src.recommendation_engine.app.domain.comments.entity.getir import (
    GetirComments,
)


def test_getir_comments():
    getir_comments = GetirComments(restaurant_id="60128f1082ce14c9bc57d68a")
    results = getir_comments.process()
    assert isinstance(results, list)
    assert len(results) > 0
