from loguru import logger

from ...entity import BaseEntity
from ...processor import Processor, SyncCallParams
from ..values import RequestValue, MenuValue, MenuStack


class GetirMenu(BaseEntity, Processor):
    HEADERS = {
        "authority": "food-client-api-gateway.getirapi.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,tr;q=0.8",
        "content-type": "application/json",
        "language": "tr",
        "origin": "https://getir.com",
        "referer": "https://getir.com/",
        "Cookie": (
            "appType=GETIR; cloudfrontHeaders=%7B%22viewerCountry%22%3A%22TR%22%2C%22lat%22%3Anull"
            "%2C%22lon%22%3Anull%7D; countryCode=TR; language=tr; locale=tr; trueClientIp=null; version=1.2.178"
        ),
    }

    def __init__(self, restaurant_slug: str):
        super().__init__()
        self.restaurant_slug = restaurant_slug
        self.filter_and_search_payload = RequestValue(
            url=(
                f"https://getir.com/_next/data/VzYFi8JbOx5ftRNvdlm-F/tr/yemekPage"
                f"/restaurants/{self.restaurant_slug}.json?slug={self.restaurant_slug}"
            ),
            method="GET",
            headers=self.HEADERS,
        )
        self.menu_stack = MenuStack()

    def _retrieve_menu_from_api(self) -> list[dict] | None:
        request_template = self.filter_and_search_payload.retrieve_formatted_request(
            {"restaurant_slug": self.restaurant_slug}
        )
        sync_call_params = SyncCallParams(**request_template)
        response = self.synchronized_call(sync_call_params)
        data = self._retrieve_json_from_response(response)

        menu_list = (
            data.get("pageProps")
            .get("initialState")
            .get("restaurantDetail")
            .get("menu")
            .get("productCategories", [])
        )
        logger.info(f"Menu with {self.restaurant_slug} was crawled.")
        return menu_list

    @staticmethod
    def _transform_unstructured_data(category: str, menu_value: dict) -> MenuValue:
        values = dict()
        values["category"] = category
        values["product_id"] = menu_value["id"]
        values["name"] = menu_value["name"]
        values["price"] = menu_value["priceText"]
        values["description"] = menu_value["description"]
        values["image_url"] = menu_value["imageURL"]
        values["full_screen_image_url"] = menu_value["fullScreenImageURL"]
        values["is_available"] = menu_value["isAvailable"]
        menu_value = MenuValue(**values)
        return menu_value

    def process(self, process_limit: int | None = None) -> list[MenuValue]:
        menu_list = self._retrieve_menu_from_api()
        for entity in menu_list:
            category = entity["name"]
            category_menu_list = entity["products"]
            for category_menu in category_menu_list:
                menu = self._transform_unstructured_data(category, category_menu)
                self.menu_stack.add_menu(menu)

            if process_limit is not None and len(self.menu_stack) >= process_limit:
                break

        return self.menu_stack.retrieve_menu_list()
