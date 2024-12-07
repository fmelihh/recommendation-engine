from pydantic import BaseModel, Field


class MenuDto(BaseModel):
    category: str | None = Field(default=None)
    product_id: str | None = Field(None)
    name: str
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    price: float
    price_currency: str
