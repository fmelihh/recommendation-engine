from src.recommendation_engine.app.domain.restaurants.values import (
    GeoValue,
)
from src.recommendation_engine.app.domain.restaurants.entity.yemek_sepeti import (
    YemeksepetiRestaurants,
)


def test_getir_restaurants():
    geo_value = GeoValue(lat=38.6748, lon=39.2225)
    yemeksepeti_restaurants = YemeksepetiRestaurants(geo_value=geo_value)
    results = yemeksepeti_restaurants.process(process_limit=1)
    assert isinstance(results, list)
    # assert len(results) > 0
