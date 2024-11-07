from dataclasses import dataclass

from ..price import Price
from ..geo import GeoValue
from ..restaurant import RestaurantValue


@dataclass(frozen=True)
class YemeksepetiRestaurantValue(RestaurantValue):
    name: str
    rating: float | int | None
    url_slug: str
    restaurant_id: str | int | float
    review_number: int | None
    coordinates: GeoValue | dict | None
    minimum_pickup_time: float | None
    minimum_order_amount: Price | float | None
    minimum_delivery_fee: Price | float | None
    minimum_delivery_time: float | str | None
    original_delivery_fee: Price | float | None
    loyalty_percentage_amount: float | None

    def validate_name(self) -> str:
        if not isinstance(self.name, str):
            raise ValueError("invalid name type expected.")

        return self.name

    def validate_rating(self) -> int | None:
        if self.rating and not isinstance(self.rating, (int, float)):
            raise ValueError("invalid rating type expected.")
        return self.rating

    def validate_url_slug(self) -> str:
        if not isinstance(self.url_slug, str):
            raise ValueError("invalid url_slug type expected.")
        return self.url_slug

    def validate_restaurant_id(self) -> str:
        if not self.restaurant_id:
            raise ValueError("invalid restaurant_id type expected.")
        return str(self.restaurant_id)

    def validate_review_number(self) -> int | None:
        if self.review_number and not isinstance(self.review_number, int):
            raise ValueError("invalid review_number type expected.")
        return self.review_number

    def validate_coordinates(self) -> GeoValue | None:
        if (
            not isinstance(self.coordinates, dict)
            or "lat" not in self.coordinates
            or "lon" not in self.coordinates
            or not isinstance(self.coordinates["lat"], float)
            or not isinstance(self.coordinates["lon"], float)
        ):
            raise ValueError("invalid coordinates type expected.")
        return GeoValue(lat=self.coordinates["lat"], lon=self.coordinates["lon"])

    def validate_minimum_pickup_time(self) -> float | None:
        if self.minimum_pickup_time and not isinstance(
            self.minimum_pickup_time, (int, float)
        ):
            raise ValueError("invalid minimum_pickup_time type expected.")

        return float(self.minimum_pickup_time)

    def validate_minimum_order_amount(self) -> Price | None:
        if self.minimum_order_amount and not isinstance(
            self.minimum_order_amount, (float, int)
        ):
            raise ValueError("invalid minimum_order_amount type expected.")

        return Price(amount=float(self.minimum_order_amount), currency="TL")

    def validate_minimum_delivery_fee(self) -> Price | None:
        if self.minimum_delivery_fee and not isinstance(
            self.minimum_delivery_fee, (float, int)
        ):
            raise ValueError("invalid minimum_delivery_fee type expected.")

        return Price(amount=float(self.minimum_delivery_fee), currency="TL")

    def validate_minimum_delivery_time(self) -> float | str | None:
        if self.minimum_delivery_time and not isinstance(
            self.minimum_delivery_time, (float, int)
        ):
            raise ValueError("invalid minimum_delivery_time type expected.")

        return str(self.minimum_delivery_time)

    def validate_original_delivery_fee(self) -> Price | None:
        if self.original_delivery_fee and not isinstance(
            self.original_delivery_fee, (float, int)
        ):
            raise ValueError("invalid original_delivery_fee type expected.")

        return Price(amount=float(self.original_delivery_fee), currency="TL")

    def validate_loyalty_percentage_amount(self) -> float | None:
        if self.loyalty_percentage_amount and not isinstance(
            self.loyalty_percentage_amount, (float, int)
        ):
            raise ValueError("invalid loyalty_percentage_amount type expected.")

        return float(self.loyalty_percentage_amount)
