from loguru import logger
from typing import Generator

from ..values import GeoValue
from ...entity import BaseEntity
from ...processor import Processor
from ...request import RequestValue
from ...processor import SyncCallParams
from ...value_stack import EntityValueStack
from ..values.yemeksepeti import YemeksepetiRestaurantValue


class YemeksepetiRestaurants(BaseEntity, Processor):
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.yemeksepeti.com",
        "perseus-client-id": "1715372289643.728421729131829214.jbyk0nystp",
        "perseus-session-id": "1715372289643.707748580212862372.cbhwjz0m2c",
        "priority": "u=1, i",
        "referer": "https://www.yemeksepeti.com/",
        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "x-pd-language-id": "2",
        "Cookie": "__cf_bm=jQUwOPufx1Ill_YuUW9Qk55HtJW7QcqU11VsXXMrZqw-1715501543-1.0.1.1-.ArnmwCY3ev_YC7_4SL8QTxNJjYAskuVnyfJJDFF3YsJAndaH3JDLtVGiFqwwD2D4HbfFY8MKynONUowZ2AIem.COi9YFpiC6bCoAVtZobM",
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
                {{
                    "filters": [
                        {{
                            "filter": "sort",
                            "value": [
                                "2"
                            ]
                        }}
                    ],
                    "location": {{
                        "lat": {lat},
                        "lon": {lon}
                    }},
                    "skip": {skip},
                    "limit": 10
                }}
            """,
        )
        self.restaurant_stack = EntityValueStack()

    # def _iterate_over_restaurants(self) -> Generator[dict, None, None]:
    #     skip = 0
    #     while 1:
    #         request_template = (
    #             self.filter_and_search_payload.retrieve_formatted_request(
    #                 {"skip": skip, "lat": self.geo_value.lat, "lon": self.geo_value.lon}
    #             )
    #         )
    #         sync_call_params = SyncCallParams(**request_template)
    #         response = self.synchronized_call(sync_call_params)
    #         data = self._retrieve_json_from_response(response)
    #
    #         if not data:
    #             break
    #
    #         restaurants = (
    #             data.get("data", {}).get("restaurantSection", {}).get("restaurants")
    #         )
    #
    #         if not restaurants:
    #             break
    #
    #         yield restaurants
    #         logger.info(
    #             f"page {skip} was crawled. total crawled data is {len(self.restaurant_stack)}"
    #         )
    #
    #         skip += 10

    @staticmethod
    def transform_unstructured_data(record_value: dict) -> YemeksepetiRestaurantValue:
        pass

    def process(
        self, process_limit: int | None = None
    ) -> list[YemeksepetiRestaurantValue]:
        pass
