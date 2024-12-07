from src.recommendation_engine.app.features.menu.domain.entity.getir import (
    GetirMenu,
)


def test_getir_menu():
    getir_menu = GetirMenu(
        restaurant_slug="burger-buffs-merkez-cumhuriyet-mah-merkez-elazig"
    )
    results = getir_menu.process(process_limit=1)
    assert isinstance(results, list)
    assert len(results) > 0
