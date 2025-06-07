from fastapi import APIRouter

from ...services.recommendation import RecommendationService

recommendation_router = APIRouter()


@recommendation_router.get("/recommend")
async def recommend(query: str, top_k: int = 3):
    result = await RecommendationService.search(query=query, top_k=top_k)
    return result
