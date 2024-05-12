from dataclasses import dataclass


@dataclass(frozen=True)
class ProductVariation:
    title: str
    unit_price: int
    description: str
    image_urls: str
