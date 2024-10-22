import uuid
from clickhouse_sqlalchemy import engines
from sqlalchemy import Column
from clickhouse_sqlalchemy.types import Int32, String, DateTime, Array

from ....shared_kernel.database.clickhouse import ClickhouseBase


class CommentsModel(ClickhouseBase):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    rating = Column(Int32)
    comment = Column(String)
    comment_id = Column(String)
    replies = Column(Array(String))
    like_count = Column(Int32)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    __table_args__ = (
        engines.MergeTree(order_by="id"),
        {"schema": "default"},
    )
