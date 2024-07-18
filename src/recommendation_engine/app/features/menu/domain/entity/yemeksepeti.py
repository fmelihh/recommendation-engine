from loguru import logger

from ..values import GeoValue
from .....shared_kernel.entity import BaseEntity
from .....shared_kernel.request import RequestValue
from ..values.yemeksepeti.menu import YemeksepetiMenuValue
from .....shared_kernel.value_stack import EntityValueStack
from .....shared_kernel.processor import Processor, SyncCallParams


class YemeksepetiMenu(BaseEntity, Processor):
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

    def __init__(self, restaurant_id: str, geo_value: GeoValue):
        super().__init__()
        self.geo_value = geo_value
        self.restaurant_id = restaurant_id
        self.menu_payload = RequestValue(
            url=(f"https://tr.fd-api.com/api/v5/vendors/{self.restaurant_id}"),
            template="""
                {{
                  "include": "menus",
                  "language_id": 2,
                  "opening_type": "delivery",
                  "basket_currency": "TRY",
                  "latitude": {lat},
                  "longitude": {lon} 
                }}
            """,
            template_loc="params",
            method="GET",
            headers=self.HEADERS,
        )
        self.menu_stack = EntityValueStack()

    def _retrieve_menu_from_api(self) -> list[dict] | None:
        request_template = self.menu_payload.retrieve_formatted_request(
            {
                "restaurant_slug": self.restaurant_id,
                "lat": self.geo_value.lat,
                "lon": self.geo_value.lon,
            }
        )
        sync_call_params = SyncCallParams(**request_template)
        response = self.synchronized_call(sync_call_params)
        data = self._retrieve_json_from_response(response)

        if not data:
            return []

        menu_list = data.get("data", {}).get("menus", [])
        if len(menu_list) > 0:
            menu_list = menu_list[0].get("menu_categories")
        logger.info(f"Menu with {self.restaurant_id} was crawled.")
        return menu_list

    @staticmethod
    def _transform_unstructured_data(
        category: str, menu_value: dict
    ) -> YemeksepetiMenuValue:
        values = dict()
        values["category"] = category
        values["product_id"] = menu_value["id"]
        values["name"] = menu_value["name"]
        values["price"] = menu_value["product_variations"]
        values["description"] = menu_value["description"]
        values["image_url"] = menu_value["file_path"]

        menu_value = YemeksepetiMenuValue(**values)
        return menu_value

    def process(self, process_limit: int | None = None) -> list[YemeksepetiMenuValue]:
        menu_list = self._retrieve_menu_from_api()
        for entity in menu_list:
            category = entity["name"]
            category_menu_list = entity["products"]
            for category_menu in category_menu_list:
                menu = self._transform_unstructured_data(category, category_menu)
                self.menu_stack.add_value(menu)

            if process_limit is not None and len(self.menu_stack) >= process_limit:
                break

        return self.menu_stack.retrieve_values()
