from abc import ABC, abstractmethod
from typing import TypeVar, List, Callable

from .entity import BaseEntity
from .domain_providers import Providers
from ..features.menu.domain.values import MenuValue
from ..features.comments.domain.values import CommentValue
from ..features.restaurants.dto.restaurants import RestaurantDto

T = TypeVar("T", *[List[RestaurantDto], List[CommentValue], List[MenuValue]])


class Extractor(ABC):
    @abstractmethod
    def crawl(self) -> TypeVar:
        pass

    @abstractmethod
    def initialize_provider(self, provider_type: Providers) -> BaseEntity:
        pass

    @abstractmethod
    def initialize_mapper_function(self, provider_type: Providers) -> Callable:
        pass
