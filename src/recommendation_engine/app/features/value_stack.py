from typing import TypeVar

from .menu.domain.values import MenuValue
from .comments.domain.values import CommentValue
from .restaurants.domain.values import RestaurantValue


Z = TypeVar("Z", RestaurantValue, CommentValue, MenuValue)


class EntityValueStack:
    def __init__(self):
        self._values = []

    def retrieve_values(self) -> list[Z]:
        return self._values

    def add_value(self, value: Z):
        self._values.append(value)

    def clean_values(self):
        self._values.clear()

    def __len__(self) -> int:
        return len(self._values)