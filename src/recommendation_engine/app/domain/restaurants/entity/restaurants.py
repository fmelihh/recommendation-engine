from abc import ABC

from ...entity import BaseEntity
from ...processor import BaseProcessor


class Restaurants(ABC, BaseEntity, BaseProcessor):
    pass
