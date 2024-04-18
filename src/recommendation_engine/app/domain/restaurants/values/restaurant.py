from dataclasses import dataclass

from .price import Price
from .delivery_time import DeliveryTime


@dataclass(frozen=True)
class RestaurantValue:
    id: str | None = None
    name: str | None = None
    slug: str | None = None
    image_url: str | None = None
    rating_point: float | None = None
    rating_count: int | None = None
    is_exceed_over_rating_count: bool = False
    min_basket_size: Price | None = None
    restaurant_min_basket_size: Price | None = None
    estimated_delivery_time: DeliveryTime | None = None
    delivery_fee: Price | None = None
