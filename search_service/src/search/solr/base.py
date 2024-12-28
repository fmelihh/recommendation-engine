import pysolr
from abc import ABC


class AbstractSolr(ABC):
    def __init__(self):
        self._client = None
        self._solr_url = None

    @property
    def solr_client(self) -> pysolr.Solr:
        if self._client is None:
            self._client = pysolr.Solr(url=self.solr_url)
            self._client.ping()
        return self._client

    @property
    def solr_url(self) -> str:
        if self._solr_url is None:
            self._solr_url = "http://localhost:8983/solr/recommendation-engine"
        return self._solr_url
