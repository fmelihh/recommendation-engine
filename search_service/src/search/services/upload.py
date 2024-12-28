from typing import Generator, Any

from ..solr.query import SolrQuery
from ..solr.schema import SolrSchema
from ..solr.collection import SolrCollection
from ..utils.constants import ConstantNamespace
from ..utils.request_mixin import SyncRequestMixin, SyncCallParams


class UploadService(SyncRequestMixin):
    def __init__(self):
        self._solr_query = None
        self._solr_schema = None
        self._solr_collection = None
        super().__init__()

    @property
    def solr_collection(self) -> SolrCollection:
        if self._solr_collection is None:
            self._solr_collection = SolrCollection()
        return self._solr_collection

    @property
    def solr_query(self) -> SolrQuery:
        if self._solr_query is None:
            self._solr_query = SolrQuery()
        return self._solr_query

    @property
    def solr_schema(self) -> SolrSchema:
        if self._solr_schema is None:
            self._solr_schema = SolrSchema()
        return self._solr_schema

    def fetch_data(self) -> Generator[dict[str, Any], None, None]:
        page = 1
        while True:
            response = self.synchronized_call(
                sync_call_params=SyncCallParams(
                    url=ConstantNamespace.DATA_WORKFLOW_AGG_DATA_API,
                    params={"page": page, "page_size": 1000},
                    method="GET",
                )
            )

            data = response.json()
            if len(data) == 0:
                break

            yield data

            page += 1

    def solr_collection_migration(self):
        self.solr_collection.execute()
        self.solr_schema.execute()

    def parse_data_to_solr(self, data: list[dict[str, Any]], reindex: bool = False):
        self.solr_query.add_data(data)
        if reindex is True:
            self.solr_query.reindex_data()
