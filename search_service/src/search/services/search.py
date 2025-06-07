from typing import Any

from ..solr.query import SolrQuery
from ..schemas.search import SearchDto
from ..utils.request_mixin import SyncRequestMixin, SyncCallParams


class SearchService(SyncRequestMixin):
    def __init__(self):
        self._solr_query = None
        SyncRequestMixin.__init__(self)

    @property
    def solr_query(self) -> SolrQuery:
        if self._solr_query is None:
            self._solr_query = SolrQuery()
        return self._solr_query

    def generate_result_from_semantic_search(
        self, query: str, top_k: int
    ) -> dict[str, Any]:
        response = self.synchronized_call(
            sync_call_params=SyncCallParams(
                url="http://localhost:8003/recommend",
                method="GET",
                params={"query": query, "top_k": top_k},
                headers={"Content-Type": "application/json"},
            )
        )

        data = response.json()
        restaurant_ids = [record["restaurant_id"] for record in data]
        return self.solr_query.get_restaurants_with_id(restaurant_ids=restaurant_ids)

    def search(self, search_dto: SearchDto) -> dict[str, Any]:
        results = self.solr_query.search(
            page=search_dto.page,
            page_size=search_dto.page_size,
            search_text=search_dto.search_text,
            search_text_and=search_dto.generate_search_text_and(),
            search_text_or=search_dto.generate_search_text_or(),
        )
        if search_dto.page != 0 or len(results) > 0:
            return results

        results = self.generate_result_from_semantic_search(
            query=search_dto.search_text,
            top_k=search_dto.page_size,
        )

        return results
