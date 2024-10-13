from loguru import logger

from ..values.getir import GetirMenuValue
from .....shared_kernel.entity import BaseEntity
from .....shared_kernel.request import RequestValue
from .....shared_kernel.value_stack import EntityValueStack
from .....shared_kernel.processor import Processor, SyncCallParams


class GetirMenu(BaseEntity, Processor):
    HEADERS = {
        'Sec-Fetch-Dest': 'empty',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Host': 'getir.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
        'Referer': 'https://getir.com/',
        'Connection': 'keep-alive',
        'Cookie': '_fbp=fb.1.1728823982487.914587202355165188; ajs_anonymous_id=432ad573-560d-46f8-aa05-c3d5d6f45b85; _ga_1GZP24F3YP=GS1.1.1728823981.1.1.1728827468.35.0.0; afUserId=2e5e0ce9-1116-4be8-a0a6-9b181ebf2b46-p; _ga=GA1.2.1425785320.1728823981; _ga_V4437MTR5M=GS1.2.1728823981.1.1.1728827467.40.0.0; _gid=GA1.2.2142768962.1728823981; appType=GETIR_FOOD; cloudfrontHeaders=%7B%22viewerCountry%22%3A%22TR%22%2C%22lat%22%3A%2238.63380%22%2C%22lon%22%3A%2239.31220%22%7D; countryCode=TR; language=tr; locale=tr; trueClientIp=null; version=1.5.0; _gcl_au=1.1.2145084125.1728824056; _gat_UA-66449776-5=1; aws-waf-token=6dcabec0-0a6e-4ee9-a238-19a51a935e19:CQoAhc1g0zZuAgAA:Vu6f0P8O2iAfgdNoohvUUU4UZzziVKkP9p0F70jh4bDA/QqLsM4LYYhHDnv9I3hrAZ5rfDpU3dGsovltHyIhAas8Gxk+2xCYMCGb/qyS+kemUOpe2/9rVQhNaU+9TyAm0z+IB0jdE/Ue2NEoGT/zXwDbt0Ez/UtfIo7AS4jf5TPICEV0Dg69sKR/; isWarehouseRequestSended=false; location=%7B%22emojiId%22%3A19%2C%22name%22%3A%22Ev%22%2C%22address%22%3A%22Cumhuriyet%2C%20170.%20Sk.%20No%3A48%2C%2023190%20El%C3%A2z%C4%B1%C4%9F%20Merkez%2FElaz%C4%B1%C4%9F%2C%20T%C3%BCrkiye%22%2C%22state%22%3A%22Elaz%C4%B1%C4%9F%22%2C%22addressType%22%3A1%2C%22lat%22%3A38.666301691871546%2C%22lon%22%3A39.15095672969747%2C%22streetName%22%3A%22170.%20Sokak%22%2C%22countryIsoCode%22%3A%22TR%22%2C%22countryName%22%3A%22T%C3%BCrkiye%22%2C%22streetNumber%22%3A%22No%3A48%22%7D; newAddress=true; _tt_enable_cookie=1; _ttp=BakRoRhFmYlB4t2wD1pg5MgnZYI; cookieConsent=%7B%22technical%22%3Atrue%2C%22functional%22%3Atrue%2C%22analytical%22%3Atrue%2C%22marketing%22%3Atrue%7D; AF_SYNC=1728823975122; appType=GETIR_FOOD; cloudfrontHeaders=%7B%22viewerCountry%22%3A%22TR%22%2C%22lat%22%3A%2238.63380%22%2C%22lon%22%3A%2239.31220%22%7D; countryCode=TR; language=tr; locale=tr; trueClientIp=null; version=1.5.0',
        'tracestate': '1460171@nr=0-1-1460171-745424659-f00956db115fd215----1728827477240',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE0NjAxNzEiLCJhcCI6Ijc0NTQyNDY1OSIsImlkIjoiZjAwOTU2ZGIxMTVmZDIxNSIsInRyIjoiYTIzN2JlMGVhOTVlODc2NTcyMGFkOGY3NWZjM2QzZWEiLCJ0aSI6MTcyODgyNzQ3NzI0MH19',
        'Priority': 'u=3, i',
        'traceparent': '00-a237be0ea95e8765720ad8f75fc3d3ea-f00956db115fd215-01'
    }

    def __init__(self, restaurant_slug: str):
        super().__init__()
        self.restaurant_slug = restaurant_slug
        self.filter_and_search_payload = RequestValue(
            url=(
                f"https://getir.com/_next/data/vwVOF9DDuYeyM3fGTxCW9/tr/yemekPage"
                f"/restaurants/{self.restaurant_slug}.json?slug={self.restaurant_slug}"
            ),
            method="GET",
            headers=self.HEADERS,
        )
        self.menu_stack = EntityValueStack()

    def _retrieve_menu_from_api(self) -> list[dict] | None:
        request_template = self.filter_and_search_payload.retrieve_formatted_request(
            {"restaurant_slug": self.restaurant_slug}
        )
        sync_call_params = SyncCallParams(**request_template)
        response = self.synchronized_call(sync_call_params)
        data = self._retrieve_json_from_response(response)

        if not data:
            return []

        menu_list = (
            data.get("pageProps", {})
            .get("initialState", {})
            .get("restaurantDetail", {})
            .get("menu", {})
            .get("productCategories", [])
        )
        logger.info(f"Menu with {self.restaurant_slug} was crawled.")
        return menu_list

    @staticmethod
    def _transform_unstructured_data(category: str, menu_value: dict) -> GetirMenuValue:
        values = dict()
        values["category"] = category
        values["product_id"] = menu_value["id"]
        values["name"] = menu_value["name"]
        values["price"] = menu_value["priceText"]
        values["description"] = menu_value["description"]
        values["image_url"] = menu_value["imageURL"]
        values["full_screen_image_url"] = menu_value["fullScreenImageURL"]
        values["is_available"] = menu_value["isAvailable"]
        menu_value = GetirMenuValue(**values)
        return menu_value

    def process(self, process_limit: int | None = None) -> list[GetirMenuValue]:
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
