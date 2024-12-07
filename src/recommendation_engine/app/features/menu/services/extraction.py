from addict import Dict
from typing import List, Callable

from ..domain.values import GeoValue
from ..domain.values.menu import MenuValue
from ..domain.entity.getir import GetirMenu
from ..dto.menu import MenuDto
from ..mappers.menu import MenuMapper
from ....shared_kernel.extractor import Extractor
from ..domain.entity.yemeksepeti import YemeksepetiMenu
from ....shared_kernel.domain_providers import Providers


class MenuExtractorService(Extractor):
    def __init__(self, provider_type: Providers, **kwargs):
        self.kwargs = Dict(**kwargs)
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
            geo_value = GeoValue(lat=self.kwargs.lat, lon=self.kwargs.lon)
            return YemeksepetiMenu(
                geo_value=geo_value, restaurant_id=self.kwargs.restaurant_id
            )
        elif provider_type == Providers.GETIR:
            return GetirMenu(restaurant_slug=self.kwargs.restaurant_slug)
        else:
            raise ValueError("Provider is not defined.")

    def crawl(self) -> List[MenuDto]:
        return [self.mapper_function(element) for element in self.provider.process()]
