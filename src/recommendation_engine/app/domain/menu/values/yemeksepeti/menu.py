from pydantic import HttpUrl
from dataclasses import dataclass

from ..price import Price
from ..menu import MenuValue


@dataclass(frozen=True)
class YemeksepetiMenuValue(MenuValue):
    category: str
    product_id: str | None
    name: str
    price: Price | float | list
    description: str
    image_url: str | None

    def validate_category(self) -> str:
        if not isinstance(self.category, str):
            raise ValueError("Invalid menu category type expected.")
        return self.category

    def validate_product_id(self) -> str:
        if not self.product_id:
            raise ValueError("Invalid menu product id type expected.")
        return str(self.product_id)

    def validate_name(self) -> str:
        if not isinstance(self.name, str):
            raise ValueError("Invalid menu name type expected.")
        return self.name

    def validate_price(self) -> Price:
        if not self.price:
            raise ValueError("Invalid menu price type expected.")

        amount = 0
        if isinstance(self.price, list):
            amount = self.price[0].get("price", 0) if len(self.price) > 0 else 0

        amount = float(amount)
        return Price(amount=amount, currency="TL")

    def validate_description(self) -> str:
        if not isinstance(self.description, str):
            raise ValueError("Invalid menu description type expected.")
        return self.description

    def validate_image_url(self) -> str | None:
        if not isinstance(self.image_url, str):
            raise ValueError("Invalid menu image url type expected.")
        if len(self.image_url) == 0:
            return None
        return str(HttpUrl(self.image_url))
