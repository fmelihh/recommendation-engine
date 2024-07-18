from typing import List

from ....shared_kernel.extractor import Extractor
from ..domain.values.restaurant import RestaurantValue


class RestaurantExtractorService(Extractor):
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def crawl(self) -> List[RestaurantValue]:
        pass
