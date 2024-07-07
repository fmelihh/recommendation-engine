from clickhouse_sqlalchemy import engines
from sqlalchemy import Column, Integer, String, Date

from ....core.database.clickhouse import ClickhouseBase


class CommentsModel(ClickhouseBase):
    __tablename__ = "comments"

    __table_args__ = (
        engines.MergeTree(order_by=["id"]),
        {"schema": "default"},
    )
