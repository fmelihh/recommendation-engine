import uuid
import pendulum
from sqlalchemy import Column
from clickhouse_sqlalchemy import engines
from clickhouse_sqlalchemy.types import Int32, String, DateTime, Array, Nullable

from ....shared_kernel.database.clickhouse import ClickhouseBase


class CommentsModel(ClickhouseBase):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String)
    rating = Column(Int32)
    comment = Column(String)
    comment_id = Column(String)
    replies = Column(Array(String))
    like_count = Column(Int32)
    created_at = Column(Nullable(DateTime))
    updated_at = Column(Nullable(DateTime))
    version = Column(Int32, default=pendulum.now("Europe/Istanbul").int_timestamp)

    __table_args__ = (
        engines.ReplacingMergeTree(order_by="id", version="version"),
        {"schema": "default"},
    )
