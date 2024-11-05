import uuid
import hashlib
from sqlalchemy import Column
from clickhouse_sqlalchemy import engines
from clickhouse_sqlalchemy.types import String, Float, Int32

from ....shared_kernel.database.clickhouse import ClickhouseBase


class RestaurantModel(ClickhouseBase):
    __tablename__ = "restaurant"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String, nullable=False)
    rating = Column(Float, nullable=True)
    restaurant_id = Column(String, nullable=False)
    delivery_fee = Column(Float, nullable=False)
    restaurant_slug = Column(String, nullable=False)
    delivery_time = Column(Float, nullable=False)
    delivery_fee_currency = Column(String, nullable=False)
    review_number = Column(Int32, nullable=False)
    image_url = Column(String, nullable=True)
    order_amount = Column(Float, nullable=True)
    order_amount_currency = Column(String, nullable=True)
    loyalty_percentage_amount = Column(Float, nullable=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    version = Column(
        String,
        nullable=False,
        default=lambda context: hashlib.md5(
            (
                context.get_current_parameters()["restaurant_id"]
                + context.get_current_parameters()["name"]
                + context.get_current_parameters()["city"]
            ).encode()
        ).hexdigest(),
    )

    __table_args__ = (
        engines.ReplacingMergeTree(order_by="id", version="version"),
        {"schema": "default"},
    )
