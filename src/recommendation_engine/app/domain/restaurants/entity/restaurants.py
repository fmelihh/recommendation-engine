from abc import ABC

from ...entity import BaseEntity
from ...processor import Processor
from ..values.restaurant_stack import RestaurantStack


class Restaurants(ABC, BaseEntity, Processor):
    def __init__(self):
        self._restaurant_stack = RestaurantStack()
