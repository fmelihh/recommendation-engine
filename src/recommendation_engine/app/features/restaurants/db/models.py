from clickhouse_sqlalchemy import engines
from sqlalchemy import Column, String, Float, Integer

from ....core.database.clickhouse import ClickhouseBase


class RestaurantModel(ClickhouseBase):
    __tablename__ = "restaurant"

    name: str = Column(String)
    rating: float = Column(Float)
    restaurant_id: str = Column(String)
    delivery_fee: float = Column(Float)
    restaurant_slug: str = Column(String)
    delivery_time: float = Column(Float)
    delivery_fee_currency: str = Column(String)
    review_number: int = Column(Integer)
    image_url: str | None = Column(String)
    order_amount: float | None = Column(Float, nullable=True)
    order_amount_currency: str | None = Column(String, nullable=True)
    loyalty_percentage_amount: float | None = Column(Float, nullable=True)

    __table_args__ = (
        engines.MergeTree(order_by=["restaurant_id"]),
        {"schema": "default"},
    )
