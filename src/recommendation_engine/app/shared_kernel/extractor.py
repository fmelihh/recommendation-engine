from typing import TypeVar, List
from abc import ABC, abstractmethod

from ..features.menu.domain.values import MenuValue
from ..features.comments.domain.values import CommentValue
from ..features.restaurants.domain.values import RestaurantValue


T = TypeVar("T", *[List[RestaurantValue], List[CommentValue], List[MenuValue]])


class Extractor(ABC):
    @abstractmethod
    def crawl(self) -> TypeVar:
        pass
