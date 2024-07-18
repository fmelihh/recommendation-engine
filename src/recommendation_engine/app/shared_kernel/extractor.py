from typing import TypeVar, List
from abc import ABC, abstractmethod

from .entity import BaseEntity
from .domain_providers import Providers
from ..features.menu.domain.values import MenuValue
from ..features.comments.domain.values import CommentValue
from ..features.restaurants.domain.values import RestaurantValue


T = TypeVar("T", *[List[RestaurantValue], List[CommentValue], List[MenuValue]])


class Extractor(ABC):
    @abstractmethod
    def crawl(self) -> TypeVar:
        pass

    @abstractmethod
    def initialize_provider(self, provider_type: Providers) -> BaseEntity:
        pass
