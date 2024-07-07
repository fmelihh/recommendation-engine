from pydantic import BaseModel, Field


class MenuDto(BaseModel):
    category: str
    product_id: str | None = Field(None)
    name: str
    description: str
    image_url: str
    price: float
    price_currency: str
