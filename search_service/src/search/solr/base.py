import pysolr
from typing import Any
from abc import ABC, abstractmethod

from ..utils.constants import ConstantNamespace
from ..utils.request_mixin import SyncRequestMixin, SyncCallParams


class AbstractExecutor(ABC):
    @abstractmethod
    def execute(self):
        pass


class AbstractSolr(ABC, SyncRequestMixin):
    def __init__(self):
        self._client = None
        self._solr_url = None
        self._base_solr_url = None

        super().__init__()

    @property
    def solr_client(self) -> pysolr.Solr:
        if self._client is None:
            self._client = pysolr.Solr(url=self.solr_url)
            self._client.ping()
        return self._client

    @property
    def solr_url(self) -> str:
        if self._solr_url is None:
            self._solr_url = (
                f"{self.base_solr_url}/{ConstantNamespace.SOLR_COLLECTION_ALIAS}"
            )
        print(self._solr_url)
        return self._solr_url

    @property
    def base_solr_url(self) -> str:
        if self._base_solr_url is None:
            self._solr_url = f"http://localhost:8983/solr"
        return self._solr_url

    def add_data(self, data: list[dict[str, Any]]):
        batch_size = 500
        for i in range(0, len(data), batch_size):
            self.solr_client.add(data[i : i + batch_size])
        self.solr_client.commit()

    def retrieve_all_data(self, start: int, rows: int) -> list[dict[str, Any]]:
        records = self.solr_client.search(q="*:*", rows=rows, start=start)
        return list(records)

    def delete_data(self, query: str = "*:*"):
        self.synchronized_call(
            sync_call_params=SyncCallParams(
                url=f"{self.solr_url}/update?commit=true",
                body=f'{{"delete": {{"query": {query}]}}}}',
                method="POST",
            )
        )

    def reindex_data(self):
        start = 0
        rows = 10000
        all_data = []
        while records := self.retrieve_all_data(start=start, rows=rows):
            all_data.extend(records)
            start += rows

        self.delete_data()
        self.solr_client.commit()
        self.solr_client.optimize()
