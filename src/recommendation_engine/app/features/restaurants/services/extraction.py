from typing import List

from ....shared_kernel.extractor import Extractor
from ..domain.values.restaurant import RestaurantValue


class RestaurantExtractorService(Extractor):
    def crawl(self) -> List[RestaurantValue]:
        pass
