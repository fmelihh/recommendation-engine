import uuid
from clickhouse_sqlalchemy import engines
from sqlalchemy import Column
from clickhouse_sqlalchemy.types import String, Float

from ....shared_kernel.database.clickhouse import ClickhouseBase


class MenuModel(ClickhouseBase):
    __tablename__ = "menu"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category= Column(String)
    product_id = Column(String)
    name = Column(String)
    description = Column(String)
    image_url = Column(String)
    price = Column(Float)
    price_currency = Column(String)

    __table_args__ = (
        engines.MergeTree(order_by="id"),
        {"schema": "default"},
    )
