from pydantic import HttpUrl
from dataclasses import dataclass

from ..price import Price
from ..rating_count import RatingCount
from ..delivery_time import DeliveryTime
from ..restaurant import RestaurantValue


@dataclass(frozen=True)
class GetirRestaurantValue(RestaurantValue):
    id: str | None = None
    name: str | None = None
    slug: str | None = None
    image_url: str | None = None
    rating_point: float | None = None
    rating_count: RatingCount | str | None = None
    min_basket_size: Price | str | None = None
    restaurant_min_basket_size: Price | str | None = None
    estimated_delivery_time: DeliveryTime | dict | None = None
    delivery_fee: Price | str | None = None

    def validate_id(self) -> str:
        if not isinstance(self.id, str):
            raise ValueError("invalid id type expected.")
        return self.id

    def validate_name(self) -> str:
        if not isinstance(self.name, str):
            raise ValueError("invalid name type expected.")
        return self.name

    def validate_slug(self) -> str:
        if not isinstance(self.slug, str):
            raise ValueError("invalid slug type expected.")
        return self.slug

    def validate_image_url(self) -> str:
        if not isinstance(self.image_url, str):
            raise ValueError("invalid image_url type expected.")

        return str(HttpUrl(self.image_url))

    def validate_rating_point(self) -> float:
        try:
            return float(self.rating_point)
        except Exception:
            raise ValueError("invalid rating point type expected.")

    def validate_rating_count(self) -> RatingCount:
        if not isinstance(self.rating_count, str):
            raise ValueError("invalid rating count type expected.")

        is_exceed_count = "+" in self.rating_count
        count = (
            self.rating_count.replace("(", "").replace(")", "").replace("+", "").strip()
        )
        return RatingCount(count=int(count), is_exceed_count=is_exceed_count)

    def validate_min_basket_size(self) -> Price | None:
        if self.min_basket_size is None:
            return None
        if not isinstance(self.min_basket_size, str):
            raise ValueError("invalid min basket size type expected.")
        amount = self.min_basket_size.replace("₺", "").replace(",", ".").strip()
        amount = float(amount)
        return Price(amount=amount, currency="TL")

    def validate_restaurant_min_basket_size(self) -> Price | None:
        if self.restaurant_min_basket_size is None:
            return None

        if not isinstance(self.restaurant_min_basket_size, str):
            raise ValueError("invalid restaurant min basket size expected.")
        amount = (
            self.restaurant_min_basket_size.replace("₺", "").replace(",", ".").strip()
        )
        amount = float(amount)
        return Price(amount=amount, currency="TL")

    def validate_estimated_delivery_time(self) -> DeliveryTime | None:
        if not isinstance(self.estimated_delivery_time, dict):
            raise ValueError("invalid estimated delivery time type expected.")
        if (
            "value" not in self.estimated_delivery_time
            and "suffix" not in self.estimated_delivery_time
        ):
            return None

        unit = self.estimated_delivery_time["suffix"].strip()
        le, ge = self.estimated_delivery_time["value"].split("-")

        le = int(le.strip())
        ge = int(ge.strip())
        return DeliveryTime(le=le, ge=ge, unit=unit)

    def validate_delivery_fee(self) -> Price | None:
        if self.delivery_fee is None:
            return None

        if not isinstance(self.delivery_fee, str):
            raise ValueError("invalid delivery fee type expected.")

        amount = float(self.delivery_fee.replace("₺", "").replace(",", ".").strip())
        return Price(amount=amount, currency="TL")
