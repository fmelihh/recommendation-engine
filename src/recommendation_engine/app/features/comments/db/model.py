from typing import TypeVar
from clickhouse_sqlalchemy import engines
from sqlalchemy import Column, Integer, String, Date

from ..domain.entity.getir import GetirComments
from ....core.database.clickhouse import ClickhouseBase
from ..domain.entity.yemek_sepeti import YemekSepetiComments


CommentEntity = TypeVar('CommentEntity', GetirComments, YemekSepetiComments)


class CommentsModel(ClickhouseBase):
    __tablename__ = 'comments'

    @staticmethod
    def from_entity(entity: CommentEntity):
        pass

    __table_args__ = (
        engines.MergeTree(order_by=['id']),
        {'schema': "default"},
    )
