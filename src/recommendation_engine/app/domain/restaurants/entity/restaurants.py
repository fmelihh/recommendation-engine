from abc import ABC

from ...entity import BaseEntity
from ...processor import Processor


class Restaurants(ABC, BaseEntity, Processor):
    pass
