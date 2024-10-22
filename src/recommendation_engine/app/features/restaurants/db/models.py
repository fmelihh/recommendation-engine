import uuid
from clickhouse_sqlalchemy import engines
from sqlalchemy import Column
from clickhouse_sqlalchemy.types import String, Float, Int32

from ....shared_kernel.database.clickhouse import ClickhouseBase


class RestaurantModel(ClickhouseBase):
    __tablename__ = "restaurant"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String)
    rating = Column(Float)
    restaurant_id = Column(String)
    delivery_fee = Column(Float)
    restaurant_slug = Column(String)
    delivery_time = Column(Float)
    delivery_fee_currency = Column(String)
    review_number = Column(Int32)
    image_url = Column(String)
    order_amount = Column(Float, nullable=True)
    order_amount_currency = Column(String, nullable=True)
    loyalty_percentage_amount = Column(Float, nullable=True)

    __table_args__ = (
        engines.MergeTree(order_by="id"),
        {"schema": "default"},
    )
