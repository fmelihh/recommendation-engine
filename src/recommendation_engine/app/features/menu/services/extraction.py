from addict import Dict
from typing import List

from ..domain.values import GeoValue
from ..domain.values.menu import MenuValue
from ..domain.entity.getir import GetirMenu
from ....shared_kernel.extractor import Extractor
from ..domain.entity.yemeksepeti import YemeksepetiMenu
from ....shared_kernel.domain_providers import Providers


class MenuExtractorService(Extractor):
    def __init__(self, provider_type: Providers, **kwargs):
        self.kwargs = Dict(**kwargs)
        self.provider = self.initialize_provider(provider_type)

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

    def crawl(self) -> List[MenuValue]:
        return self.provider.process()
