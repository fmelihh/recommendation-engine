import os


class ConstantNamespace:
    SOLR_COLLECTION_ALIAS = os.getenv("SOLR_COLLECTION_ALIAS", "recom")
    DATA_WORKFLOW_AGG_DATA_API = os.getenv(
        "DATA_WORKFLOW_AGG_DATA_API", "localhost:8000/aggregate_domain/aggregate_data"
    )
