from fastapi import APIRouter

from ....features.kernel.services.recommendation_aggregate_domains import (
    RecommendationAggregateDomainsService,
)

recommendation_aggregate_domain_router = APIRouter()


@recommendation_aggregate_domain_router.get("/recommendation-aggregate-data")
def aggregate_data(page: int = 1, page_size: int = 10):
    return RecommendationAggregateDomainsService.retrieve_aggregate_data_detail(
        page, page_size
    )
