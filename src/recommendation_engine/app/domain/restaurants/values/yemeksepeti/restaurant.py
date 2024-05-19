from dataclasses import dataclass

from ..restaurant import RestaurantValue


@dataclass(frozen=True)
class YemeksepetiRestaurantValue(RestaurantValue):
    pass
