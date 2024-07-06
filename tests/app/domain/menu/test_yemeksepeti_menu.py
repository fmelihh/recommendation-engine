from src.recommendation_engine.app.domain.menu.entity.yemeksepeti import (
    YemeksepetiMenu,
    GeoValue,
)


def test_yemeksepeti_menu():
    yemeksepeti_menu = YemeksepetiMenu(
        restaurant_id="b6is", geo_value=GeoValue(lat=38.6630978, lon=39.1869962)
    )
    results = yemeksepeti_menu.process(process_limit=1)
    assert isinstance(results, list)
    assert len(results) > 0
