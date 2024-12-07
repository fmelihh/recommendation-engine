import uuid
import pendulum
from sqlalchemy import Column
from clickhouse_sqlalchemy import engines
from clickhouse_sqlalchemy.types import String, Float, Int32, Nullable

from ....shared_kernel.database.clickhouse import ClickhouseBase


class MenuModel(ClickhouseBase):
    __tablename__ = "menu"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category = Column(String)
    product_id = Column(Nullable(String))
    name = Column(String)
    description = Column(String)
    image_url = Column(String)
    price = Column(Float)
    price_currency = Column(String)
    version = Column(Int32, default=pendulum.now("Europe/Istanbul").int_timestamp)

    __table_args__ = (
        engines.ReplacingMergeTree(order_by="id", version="version"),
        {"schema": "default"},
    )
