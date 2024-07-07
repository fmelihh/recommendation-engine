from clickhouse_sqlalchemy import engines
from sqlalchemy import Column, String, Float

from ....core.database.clickhouse import ClickhouseBase


class MenuModel(ClickhouseBase):
    __tablename__ = "comments"

    category: str = Column(String)
    product_id: str | None = Column(String)
    name: str = Column(String)
    description: str = Column(String)
    image_url: str = Column(String)
    price: float = Column(Float)
    price_currency: str = Column(String)

    __table_args__ = (
        engines.MergeTree(order_by=["product_id"]),
        {"schema": "default"},
    )
