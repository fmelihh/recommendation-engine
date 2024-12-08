from pysolr import Solr


class SolrQuery:
    def __init__(self):
        self._client = Solr(
            url="http://localhost:8983/solr/recommendation-engine",
        )
        self._client.ping()
