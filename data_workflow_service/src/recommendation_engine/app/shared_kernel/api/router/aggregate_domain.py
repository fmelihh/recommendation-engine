from fastapi import APIRouter

from ....features.kernel.services.aggregate_domains import AggregateDomainsService

aggregate_domain_router = APIRouter()


@aggregate_domain_router.get("/aggregate-data")
def aggregate_data(page: int = 1, page_size: int = 10):
    return AggregateDomainsService.retrieve_aggregate_data(page, page_size)


@aggregate_domain_router.get("/aggregate-data-detail")
def aggregate_data_detail(restaurant_id: str):
    return AggregateDomainsService.retrieve_aggregate_data_detail(restaurant_id)
