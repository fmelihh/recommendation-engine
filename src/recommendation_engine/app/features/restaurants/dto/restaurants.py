from pydantic import BaseModel, Field


class RestaurantDto(BaseModel):
    name: str
    rating: float | None = Field(default=None)
    restaurant_id: str
    delivery_fee: float | None = Field(default=None)
    restaurant_slug: str
    delivery_time: str | None = Field(default=None)
    delivery_fee_currency: str | None = Field(default=None)
    review_number: int = Field(default=0)
    image_url: str | None = Field(default=None)
    order_amount: float | None = Field(default=None)
    order_amount_currency: str | None = Field(default=None)
    loyalty_percentage_amount: float | None = Field(default=None)
    lat: float | None = Field(default=None)
    long: float | None = Field(default=None)
