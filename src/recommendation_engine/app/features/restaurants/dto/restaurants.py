from pydantic import BaseModel, Field


class RestaurantDto(BaseModel):
    name: str
    rating: float
    restaurant_id: str
    delivery_fee: float
    restaurant_slug: str
    delivery_time: float
    delivery_fee_currency: str
    review_number: int = Field(default=0)
    image_url: str | None = Field(default=None)
    order_amount: float | None = Field(default=None)
    order_amount_currency: str | None = Field(default=None)
    loyalty_percentage_amount: float | None = Field(default=None)
