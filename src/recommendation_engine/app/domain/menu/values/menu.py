from pydantic import HttpUrl
from dataclasses import dataclass

from .price import Price
from ...mixins import DataclassValidationMixin


@dataclass(frozen=True)
class MenuValue(DataclassValidationMixin):
    category: str
    product_id: str
    name: str
    price: Price
    description: str
    image_url: str | None
    full_screen_image_url: str | None
    is_available: bool

    def validate_category(self) -> str:
        if not isinstance(self.category, str):
            raise ValueError("Invalid comment category type expected.")
        return self.category

    def validate_product_id(self) -> str:
        if not isinstance(self.product_id, str):
            raise ValueError("Invalid comment product id type expected.")
        return self.product_id

    def validate_name(self) -> str:
        if not isinstance(self.name, str):
            raise ValueError("Invalid comment name type expected.")
        return self.name

    def validate_price(self) -> Price:
        if not isinstance(self.price, str):
            raise ValueError("Invalid comment price type expected.")

        amount = self.price.replace("₺", "").replace(",", ".").strip()
        amount = float(amount)
        return Price(amount=amount, currency="TL")

    def validate_description(self) -> str:
        if not isinstance(self.description, str):
            raise ValueError("Invalid comment description type expected.")
        return self.description

    def validate_image_url(self) -> str | None:
        if not isinstance(self.image_url, str):
            raise ValueError("Invalid comment image url type expected.")
        if len(self.image_url) == 0:
            return None
        return str(HttpUrl(self.image_url))

    def validate_full_screen_image_url(self) -> str | None:
        if not isinstance(self.full_screen_image_url, str):
            raise ValueError("Invalid comment full_screen_image_url type expected.")
        if len(self.full_screen_image_url) == 0:
            return None
        return str(HttpUrl(self.full_screen_image_url))

    def validate_is_available(self) -> bool:
        if not isinstance(self.is_available, bool):
            raise ValueError("Invalid comment is available type expected.")
        return self.is_available
