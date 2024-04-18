from .restaurants import Restaurants
from ...processor import SyncCallParams
from ..values import GeoValue, RequestValue, RestaurantValue


class GetirRestaurants(Restaurants):
    def __init__(self, geo_value: GeoValue) -> None:
        super().__init__()
        self.geo_value = geo_value
        self.getir_restaurants = []
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
