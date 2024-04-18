from dataclasses import dataclass
from .restaurant import RestaurantValue


@dataclass(frozen=True)
class RestaurantStack:
    _restaurants = []

    def retrieve_restaurants(self) -> list[RestaurantValue]:
        return self._restaurants

    def add_restaurant(self, restaurant_value: RestaurantValue):
        self._restaurants.append(restaurant_value)

    def __len__(self) -> int:
        return len(self._restaurants)

    def clean_restaurants(self):
        self._restaurants.clear()
