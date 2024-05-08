from src.recommendation_engine.app.domain.menu.entity.getir import (
    GetirMenu,
)


def test_getir_comments():
    getir_comments = GetirMenu(
        restaurant_slug="my-doner-elazig-atasehir-mah-merkez-elazig"
    )
    results = getir_comments.process()
    assert isinstance(results, list)
    assert len(results) > 0
