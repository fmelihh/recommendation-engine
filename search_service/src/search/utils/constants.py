import os


class ConstantNamespace:
    SOLR_COLLECTION_ALIAS = os.getenv("SOLR_COLLECTION_ALIAS", "recomv2")
    DATA_WORKFLOW_AGG_DATA_API = os.getenv(
        "DATA_WORKFLOW_AGG_DATA_API",
        "http://localhost:8000/aggregate_domain/aggregate-data",
    )
