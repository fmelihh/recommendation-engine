from typing import List

from ..domain.values import GeoValue
from ....shared_kernel.extractor import Extractor
from ..domain.entity.getir import GetirRestaurants
from ..domain.values.restaurant import RestaurantValue
from ....shared_kernel.domain_providers import Providers
from ..domain.entity.yemek_sepeti import YemeksepetiRestaurants


class RestaurantExtractorService(Extractor):
    def __init__(self, provider_type: Providers, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.provider = self.initialize_provider(provider_type)

    def initialize_provider(
        self, provider_type: Providers
    ) -> YemeksepetiRestaurants | GetirRestaurants:
        geo_value = GeoValue(lat=self.lat, lon=self.lon)
        if provider_type == Providers.YEMEK_SEPETI:
            return YemeksepetiRestaurants(geo_value)
        elif provider_type == Providers.GETIR:
            return GetirRestaurants(geo_value)
        else:
            ValueError("Provider is not defined.")

    def crawl(self) -> List[RestaurantValue]:
        return self.provider.process()
