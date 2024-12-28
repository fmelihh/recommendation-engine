import datetime
from .base import AbstractSolr
from ..utils.constants import ConstantNamespace
from ..utils.request_mixin import SyncCallParams


class SolrCollection(AbstractSolr):
    def __init__(self):
        super().__init__()

    def execute(self):
        new_collection_name = self._create_collection()
        self._bind_collection_with_alias(new_collection_name)

    def _create_collection(self) -> str:
        new_collection_name = f"{ConstantNamespace.SOLR_COLLECTION_ALIAS}_{datetime.datetime.now().timestamp()}"
        response = self.synchronized_call(
            sync_call_params=SyncCallParams(
                url=f"{self.base_solr_url}/admin/collections",
                params={
                    "action": "CREATE",
                    "name": new_collection_name,
                    "collection.configName": "_default",
                },
                method="POST",
            )
        )
        response.raise_for_status()
        return new_collection_name

    def _bind_collection_with_alias(self, collection_name: str):
        response = self.synchronized_call(
            sync_call_params=SyncCallParams(
                url=f"{self.base_solr_url}/admin/collections",
                params={
                    "action": "CREATEALIAS",
                    "name": ConstantNamespace.SOLR_COLLECTION_ALIAS,
                    "collections": collection_name,
                },
                method="POST",
            )
        )
        response.raise_for_status()
