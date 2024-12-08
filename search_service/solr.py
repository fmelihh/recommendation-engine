from typing import Any
from pysolr import Solr


class SolrQuery:
    def __init__(self):
        self._client = Solr(
            url="http://localhost:8983/solr/recommendation-engine",
        )
        self._client.ping()

    def data_upload(self, data: list[dict[str, Any]]):
        self._client.add(data)
        self._client.commit()
        self._client.optimize()
