from dataclasses import dataclass

from ..price import Price
from ..geo import GeoValue
from ..restaurant import RestaurantValue


@dataclass(frozen=True)
class YemeksepetiRestaurantValue(RestaurantValue):
    name: str
    rating: int | None
    url_slug: str
    restaurant_id: str
    review_number: int | None
    coordinates: GeoValue | dict | None
    minimum_pickup_time: float | None
    minimum_order_amount: Price | float
    minimum_delivery_fee: Price | float
    minimum_delivery_time: float | None
    original_delivery_fee: Price | float
    loyalty_percentage_amount: float
