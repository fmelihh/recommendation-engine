from loguru import logger
from typing import Generator
from .restaurants import Restaurants
from ...processor import SyncCallParams
from ..values import GeoValue, RequestValue, RestaurantValue, RestaurantStack


class GetirRestaurants(Restaurants):
    HEADERS = {
        "authority": "food-client-api-gateway.getirapi.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,tr;q=0.8",
        "content-type": "application/json",
        "language": "tr",
        "origin": "https://getir.com",
        "referer": "https://getir.com/",
    }

    def __init__(self, geo_value: GeoValue) -> None:
        super().__init__()
        self.geo_value = geo_value
        self.filter_and_search_payload = RequestValue(
            url="https://food-client-api-gateway.getirapi.com/restaurants/filter-and-search",
            method="POST",
            template_loc="body",
            headers=self.HEADERS,
            template="""
                "filters": [
                    {
                        "filter": "sort",
                        "value": [
                            "2"
                        ]
                    }
                ],
                "location": {
                    "lat": {lat},
                    "lon": {lon}
                },
                "skip": {skip},
                "limit": 10
            """,
        )
        self.restaurant_stack = RestaurantStack()

    def _iterate_over_restaurants(self) -> Generator[dict, None, None]:
        skip = 0
        while 1:
            request_template = (
                self.filter_and_search_payload.retrieve_formatted_request(
                    {"skip": skip}
                )
            )
            sync_call_params = SyncCallParams(**request_template)
            response = self.synchronized_call(sync_call_params)
            data = self._retrieve_json_from_response(response)

            if not data:
                break

            restaurants = (
                data.get("data", {}).get("restaurantSection", {}).get("restaurants")
            )

            if not restaurants:
                break

            yield restaurants
            logger.info(
                f"page {skip} was crawled. total crawled data is {len(self.restaurant_stack)}"
            )

            skip += 10

    @staticmethod
    def transform_unstructured_data(record_value: dict) -> RestaurantValue:
        values = dict()
        values["id"] = record_value.get("id")
        values["name"] = record_value.get("name")
        values["slug"] = record_value.get("slug")
        values["image_url"] = record_value.get("imageURL")
        values["rating_point"] = record_value.get("ratingPoint")
        values["rating_count"] = record_value.get("ratingCount")
        values["min_basket_size"] = record_value.get("minBasketSize", {}).get("value")
        values["restaurant_min_basket_size"] = record_value.get(
            "restaurantMinBasketSize", {}
        ).get("value")
        values["estimated_delivery_time"] = record_value.get(
            "estimatedDeliveryDuration", {}
        )
        values["delivery_fee"] = record_value.get("deliveryFee")
        restaurant_value = RestaurantValue(**values)
        return restaurant_value

    def process(self) -> list[RestaurantValue]:
        for restaurant_list in self._iterate_over_restaurants():
            for restaurant in restaurant_list:
                restaurant = self.transform_unstructured_data(restaurant)
                self.restaurant_stack.add_restaurant(restaurant)

        return self.restaurant_stack.retrieve_restaurants()
