from dataclasses import dataclass


@dataclass(frozen=True)
class ProductVariation:
    product_variation_id: str | None
    title: str | None
    unit_price: int | None
    description: str | None
    image_urls: str | None
