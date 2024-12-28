import pysolr
from abc import ABC


class AbstractSolr(ABC):
    def __init__(self):
        self._client = pysolr.Solr(
            url="http://localhost:8983/solr/recommendation-engine",
        )
        self._client.ping()
