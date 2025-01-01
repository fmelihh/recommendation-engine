from fastapi import APIRouter, Depends

from ...schemas.search import SearchDto
from ...services.search import SearchService

search_router = APIRouter()


@search_router.get("/search_text")
async def search(search_dto: SearchDto = Depends()):
    service = SearchService()
    results = service.search(search_dto=search_dto)
    return {
        "results": results
    }
