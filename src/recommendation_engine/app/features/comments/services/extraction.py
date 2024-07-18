from addict import Dict
from typing import List

from ..domain.values.comment import CommentValue
from ..domain.entity.getir import GetirComments
from ....shared_kernel.extractor import Extractor
from ..domain.entity.yemek_sepeti import YemekSepetiComments
from ....shared_kernel.domain_providers import Providers


class CommentsExtractorService(Extractor):
    def __init__(self, provider_type: Providers, **kwargs):
        self.kwargs = Dict(**kwargs)
        self.provider = self.initialize_provider(provider_type)

    def initialize_provider(
        self, provider_type: Providers
    ) -> GetirComments | YemekSepetiComments:
        if provider_type == Providers.YEMEK_SEPETI:
            return YemekSepetiComments(restaurant_id=self.kwargs.restaurant_id)
        elif provider_type == Providers.GETIR:
            return GetirComments(restaurant_id=self.kwargs.restaurant_id)
        else:
            ValueError("Provider is not defined.")

    def crawl(self) -> List[CommentValue]:
        return self.provider.process()
