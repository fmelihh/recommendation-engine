from src.recommendation_engine.app.features.restaurants.dto.restaurants import (
    RestaurantDto,
)
from src.recommendation_engine.app.features.restaurants.mappers.restaurants import (
    RestaurantMapper,
)
from src.recommendation_engine.app.features.restaurants.domain.values.getir import (
    GetirRestaurantValue,
)
from src.recommendation_engine.app.features.restaurants.domain.values.yemeksepeti import (
    YemeksepetiRestaurantValue,
)


def test_getir_mapper():
    getir_domain_value = GetirRestaurantValue(
        id="a",
        name="a",
        slug="a",
        image_url="https://localhost.com",
        rating_point=0.0,
        rating_count="31",
        min_basket_size="31",
        restaurant_min_basket_size="31",
        estimated_delivery_time={"suffix": "a", "value": "2-3"},
        delivery_fee="1",
    )
    res = RestaurantMapper.getir_restaurant_to_dto(value_object=getir_domain_value)
    assert isinstance(res, RestaurantDto)


def test_yemeksepeti_mapper():
    yemeksepeti_domain_value = YemeksepetiRestaurantValue(
        name="a",
        rating=3,
        url_slug="a",
        restaurant_id="a",
        review_number=1,
        coordinates={"lat": 1.1, "lon": 1.1},
        minimum_pickup_time=1,
        minimum_order_amount=1,
        minimum_delivery_fee=1,
        minimum_delivery_time=1,
        original_delivery_fee=1,
        loyalty_percentage_amount=1,
    )

    res = RestaurantMapper.yemeksepeti_restaurant_to_dto(
        value_object=yemeksepeti_domain_value
    )
    assert isinstance(res, RestaurantDto)
