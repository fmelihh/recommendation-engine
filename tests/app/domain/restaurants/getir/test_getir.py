from src.recommendation_engine.app.domain.restaurants.values import (
    GeoValue,
)
from src.recommendation_engine.app.domain.restaurants.entity.getir import (
    GetirRestaurants,
)


def test_getir_restaurants():
    geo_value = GeoValue(lat=38.6748, lon=39.2225)
    getir_restaurants = GetirRestaurants(geo_value=geo_value)
    results = getir_restaurants.process(process_limit=1)
    assert isinstance(results, list)
