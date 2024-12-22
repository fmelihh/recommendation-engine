from fastapi import APIRouter

aggregate_domain_router = APIRouter()


@aggregate_domain_router.get("/aggregate-data")
def retrieve_aggregate_data(page: int = 1, page_size: int = 10):
    pass
