from typing import List, Callable

from ..dto.menu import MenuDto
from ..domain.values import GeoValue
from ..domain.entity.getir import GetirMenu
from ..mappers.menu import MenuMapper
from ....shared_kernel.extractor import Extractor
from ..domain.entity.yemeksepeti import YemeksepetiMenu
from ....shared_kernel.domain_providers import Providers


class MenuExtractorService(Extractor):
    def __init__(
        self,
        provider_type: Providers,
        lat: float | None = None,
        lon: float | None = None,
        restaurant_slug: str | None = None,
        restaurant_id: str | None = None,
    ):
        self.lat = lat
        self.lon = lon
        self.restaurant_id = restaurant_id
        self.restaurant_slug = restaurant_slug

        self.provider = self.initialize_provider(provider_type)
        self.mapper_function = self.initialize_mapper_function(provider_type)

    def initialize_mapper_function(self, provider_type: Providers) -> Callable:
        if provider_type == Providers.YEMEK_SEPETI:
            return MenuMapper.yemeksepeti_menu_to_dto
        elif provider_type == Providers.GETIR:
            return MenuMapper.getir_menu_to_dto
        else:
            raise ValueError("Provider is not defined.")

    def initialize_provider(
        self, provider_type: Providers
    ) -> YemeksepetiMenu | GetirMenu:
        if provider_type == Providers.YEMEK_SEPETI:
            geo_value = GeoValue(lat=self.lat, lon=self.lon)
            return YemeksepetiMenu(
                geo_value=geo_value, restaurant_id=self.restaurant_id
            )
        elif provider_type == Providers.GETIR:
            return GetirMenu(restaurant_slug=self.restaurant_slug)
        else:
            raise ValueError("Provider is not defined.")

    def crawl(self) -> List[MenuDto]:
        return [self.mapper_function(element) for element in self.provider.process()]
