from typing import List, Callable

from ..dto.comment import CommentDto
from ..mappers.comment import CommentMapper
from ..domain.entity.getir import GetirComments
from ....shared_kernel.extractor import Extractor
from ....shared_kernel.domain_providers import Providers
from ..domain.entity.yemek_sepeti import YemekSepetiComments


class CommentsExtractorService(Extractor):
    def __init__(self, provider_type: Providers, restaurant_id: str):
        self.restaurant_id = restaurant_id
        self.provider = self.initialize_provider(provider_type)
        self.mapper_function = self.initialize_mapper_function(provider_type)

    def initialize_mapper_function(self, provider_type: Providers) -> Callable:
        if provider_type == Providers.YEMEK_SEPETI:
            return CommentMapper.yemeksepeti_comment_to_dto
        elif provider_type == Providers.GETIR:
            return CommentMapper.getir_comment_to_dto
        else:
            raise ValueError("Provider is not defined.")

    def initialize_provider(
        self, provider_type: Providers
    ) -> GetirComments | YemekSepetiComments:
        if provider_type == Providers.YEMEK_SEPETI:
            return YemekSepetiComments(restaurant_id=self.restaurant_id)
        elif provider_type == Providers.GETIR:
            return GetirComments(restaurant_id=self.restaurant_id)
        else:
            raise ValueError("Provider is not defined.")

    def crawl(self) -> List[CommentDto]:
        return [self.mapper_function(element) for element in self.provider.process()]
