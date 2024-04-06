from ..values import GeoValue
from .restaurant import Restaurant


class GetirRestaurant(Restaurant):
    REQUEST_PAYLOAD: str = """
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
    """

    def __init__(self, geo_value: GeoValue) -> None:
        super().__init__()
        self.source = {}
        self.geo_value = geo_value

    def process():
        pass