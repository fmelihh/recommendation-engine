from ...entity import BaseEntity
from ..values import RequestValue
from ...processor import Processor, T


class GetirMenu(BaseEntity, Processor):
    HEADERS = {
        "authority": "food-client-api-gateway.getirapi.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,tr;q=0.8",
        "content-type": "application/json",
        "language": "tr",
        "origin": "https://getir.com",
        "referer": "https://getir.com/",
    }

    def __init__(self, restaurant_slug: str):
        super().__init__()
        self.restaurant_slug = restaurant_slug
        self.filter_and_search_payload = RequestValue(
            url=(
                f"https://getir.com/_next/data/VzYFi8JbOx5ftRNvdlm-F/tr/yemekPage"
                f"/restaurants/{self.restaurant_slug}.json"
            ),
            method="GET",
            template_loc="params",
            headers=self.HEADERS,
            template="""
                        {{
                            "slug": {restaurant_slug}
                        }}
                    """,
        )

    def process(self, process_limit: int | None = None) -> T:
        pass
