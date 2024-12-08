from typing import Any
from pysolr import Solr


class SolrQuery:
    def __init__(self):
        self._client = Solr(
            url="http://localhost:8983/solr/recommendation-engine",
        )
        self._client.ping()

    def data_upload(self, data: list[dict[str, Any]]):
        for record in data:
            self._client.add(record)

        self._client.commit()
