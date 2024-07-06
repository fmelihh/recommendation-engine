from src.recommendation_engine.app.features.comments.domain.entity.yemek_sepeti import (
    YemekSepetiComments,
)


def test_yemeksepeti_comments():
    yemek_sepeti_comments = YemekSepetiComments(restaurant_id="nrp4")
    results = yemek_sepeti_comments.process(process_limit=1)
    assert isinstance(results, list)
    assert len(results) > 0
