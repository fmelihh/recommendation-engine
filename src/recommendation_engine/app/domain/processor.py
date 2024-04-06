from typing import TypeVar
from abc import ABC, abstractmethod

from .restaurants.values import RestaurantValue


T = TypeVar("T", RestaurantValue)


class Processor(ABC):
    @abstractmethod
    def process() -> T | list[T]:
        pass
