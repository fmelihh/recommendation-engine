from src.recommendation_engine.app.domain.menu.entity.getir import (
    GetirMenu,
)


def test_getir_comments():
    getir_comments = GetirMenu(
        restaurant_slug="my-doner-elazig-atasehir-mah-merkez-elazig"
    )
    results = getir_comments.process(process_limit=1)
    assert isinstance(results, list)
    assert len(results) > 0
