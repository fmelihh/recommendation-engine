from .model import retrieve_recommendation_model


class RecommendationService:
    @staticmethod
    async def search(query: str, top_k=3):
        return retrieve_recommendation_model().semantic_search(query=query, top_k=top_k)
