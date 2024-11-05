from typing import List, Callable

from ..domain.values import GeoValue
from ..dto.restaurants import RestaurantDto
from ....shared_kernel.extractor import Extractor
from ..mappers.restaurants import RestaurantMapper
from ..domain.entity.getir import GetirRestaurants
from ....shared_kernel.domain_providers import Providers
from ..domain.entity.yemek_sepeti import YemeksepetiRestaurants


class RestaurantExtractorService(Extractor):
    def __init__(self, provider_type: Providers, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.provider = self.initialize_provider(provider_type)
        self.mapper_function = self.initialize_mapper_function(provider_type)

    def initialize_mapper_function(self, provider_type: Providers) -> Callable:
        if provider_type == Providers.YEMEK_SEPETI:
            return RestaurantMapper.yemeksepeti_restaurant_to_dto
        elif provider_type == Providers.GETIR:
            return RestaurantMapper.getir_restaurant_to_dto
        else:
            raise ValueError("Provider is not defined.")

    def initialize_provider(
        self, provider_type: Providers
    ) -> YemeksepetiRestaurants | GetirRestaurants:
        geo_value = GeoValue(lat=self.lat, lon=self.lon)
        if provider_type == Providers.YEMEK_SEPETI:
            return YemeksepetiRestaurants(geo_value)
        elif provider_type == Providers.GETIR:
            return GetirRestaurants(geo_value)
        else:
            raise ValueError("Provider is not defined.")

    def crawl(self) -> List[RestaurantDto]:
        return [self.mapper_function(element) for element in self.provider.process()]
