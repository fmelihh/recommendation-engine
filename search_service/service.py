from typing import Literal
from solr import SolrQuery


class SearchService:
    def __init__(self, kind: Literal["restaurant", "comment", "menu"]):
        self.kind = kind
        self._solr_query = None

    @property
    def solr_query(self) -> SolrQuery:
        if self._solr_query is None:
            self._solr_query = SolrQuery()
        return self._solr_query

    def search_restaurant(self):
        pass
