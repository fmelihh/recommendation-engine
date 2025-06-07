from typing import Any
from ..solr.query import SolrQuery
from ..schemas.search import SearchDto


class SearchService:
    def __init__(self):
        self._solr_query = None

    @property
    def solr_query(self) -> SolrQuery:
        if self._solr_query is None:
            self._solr_query = SolrQuery()
        return self._solr_query

    def search(self, search_dto: SearchDto) -> dict[str, Any]:
        return self.solr_query.search(
            page=search_dto.page,
            page_size=search_dto.page_size,
            search_text=search_dto.search_text,
            search_text_and=search_dto.generate_search_text_and(),
            search_text_or=search_dto.generate_search_text_or(),
            lat=search_dto.lat,
            lon=search_dto.lon,
        )
