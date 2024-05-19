from dataclasses import dataclass

from ..price import Price
from ..geo import GeoValue
from ..restaurant import RestaurantValue


@dataclass(frozen=True)
class YemeksepetiRestaurantValue(RestaurantValue):
    name: str
    rating: int
    url_slug: str
    restaurant_id: str
    review_number: int
    coordinates: GeoValue
    minimum_pickup_time: float
    minimum_order_amount: Price
    minimum_delivery_fee: Price
    minimum_delivery_time: float
    original_deliveriy_fee: Price
    loyalty_percentage_amount: float
