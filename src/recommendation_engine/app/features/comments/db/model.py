import datetime
from clickhouse_sqlalchemy import engines
from sqlalchemy import Column, Integer, String, DateTime, Array

from ....shared_kernel.database.clickhouse import ClickhouseBase


class CommentsModel(ClickhouseBase):
    __tablename__ = "comments"

    rating: int = Column(Integer)
    comment: str = Column(String)
    comment_id: str = Column(String)
    replies: list[str] = Column(Array(String))
    like_count: int = Column(Integer)
    created_at: datetime.datetime | None = Column(DateTime, nullable=True)
    updated_at: datetime.datetime | None = Column(DateTime, nullable=True)

    __table_args__ = (
        engines.MergeTree(order_by=["created_at"]),
        {"schema": "default"},
    )
