import tqdm
from .restaurants import Restaurants
from ...processor import SyncCallParams
from ..values import GeoValue, RequestValue, RestaurantValue


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
                "limit": {limit}
            """,
        )

    def process(self) -> list[RestaurantValue]:
        pass
