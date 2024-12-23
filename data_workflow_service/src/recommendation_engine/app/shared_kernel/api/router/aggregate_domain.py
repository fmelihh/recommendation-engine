from fastapi import APIRouter

from ....features.kernel.services.aggregate_domains import AggregateDomainsService

aggregate_domain_router = APIRouter()


@aggregate_domain_router.get("/aggregate-data")
def retrieve_aggregate_data(page: int = 1, page_size: int = 10):
    return AggregateDomainsService.retrieve_aggregate_data(page, page_size)
