from dataclasses import dataclass

from .price import Price
from ...mixins import DataclassValidationMixin


@dataclass(frozen=True)
class Menu(DataclassValidationMixin):
    category: str
    product_id: str
    name: str
    price: Price
    description: str
    image_url: str
    full_screen_image_url: str
    is_available: bool
