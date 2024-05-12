from src.recommendation_engine.app.domain.comments.entity.yemek_sepeti import (
    YemekSepetiComments,
)


def test_yemeksepeti_comments():
    yemek_sepeti_comments = YemekSepetiComments(restaurant_id="nrp4")
    results = yemek_sepeti_comments.process()
    assert isinstance(results, list)
    assert len(results) > 0
