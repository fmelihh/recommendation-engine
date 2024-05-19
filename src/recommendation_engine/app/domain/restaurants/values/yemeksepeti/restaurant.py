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
    minimum_order_amount: Price | float | None
    minimum_delivery_fee: Price | float | None
    minimum_delivery_time: float | None
    original_delivery_fee: Price | float | None
    loyalty_percentage_amount: float | None

    def validate_name(self) -> str:
        pass

    def validate_rating(self) -> int | None:
        pass

    def validate_url_slug(self) -> str:
        pass

    def validate_restaurant_id(self) -> str:
        pass

    def validate_review_number(self) -> int | None:
        pass

    def validate_coordinates(self) -> GeoValue | None:
        pass

    def validate_minimum_pickup_time(self) -> float | None:
        pass

    def validate_minimum_order_amount(self) -> Price | None:
        pass

    def validate_minimum_delivery_fee(self) -> Price | None:
        pass

    def validate_minimum_delivery_time(self) -> float | None:
        pass

    def validate_original_delivery_fee(self) -> Price | None:
        pass

    def validate_loyalty_percentage_amount(self) -> float | None:
        pass
