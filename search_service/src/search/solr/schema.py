import json
from typing import Any

from .base import AbstractSolr, AbstractExecutor
from ..utils.request_mixin import SyncCallParams


class SolrSchema(AbstractSolr, AbstractExecutor):
    def __init__(self):
        super().__init__()

    def execute(self):
        payload = dict()
        payload.update(self.fuzzy_search_field_type())
        payload.update(self.search_fields())

        self.synchronized_call(
            sync_call_params=SyncCallParams(
                url=f"{self.solr_url}/schema",
                body=payload,
                method="POST",
                headers={"Content-Type": "application/json"},
                params={"commit": "false"},
            )
        )

        print("schema creation successfully completed.")

    @staticmethod
    def fuzzy_search_field_type() -> dict[str, Any]:
        return {
            "add-field-type": [
                {
                    "name": "fuzzyFieldType",
                    "class": "solr.TextField",
                    "analyzer": {
                        "tokenizer": {"name": "whitespace"},
                        "filters": [
                            {"name": "lowercase"},
                            {"name": "classic"},
                            {"name": "nGram", "minGramSize": "3", "maxGramSize": "5"},
                        ],
                    },
                }
            ]
        }

    @staticmethod
    def search_fields() -> dict[str, Any]:
        multivalued_fields = [
            "comments",
            "product_categories",
            "product_names",
            "product_description",
        ]

        str_fields = ["restaurant_id", "lat", "lon"]
        fuzzy_fields = [
            "provider",
            "restaurant_name",
            "restaurant_city",
            "comments",
            "product_categories",
            "product_names",
            "product_description",
        ]
        int_fields = ["review_number"]
        float_fields = ["restaurant_rate", "comment_avg_rating"]

        payload_declarations = []
        for str_field in str_fields:
            payload_declarations.append(
                {"name": str_field, "type": "string", "multiValued": False}
            )
        for float_field in [*float_fields, *int_fields]:
            payload_declarations.append(
                {"name": float_field, "type": "plongs", "multiValued": False}
            )
        for fuzzy_field in fuzzy_fields:
            if fuzzy_field not in multivalued_fields:
                payload_declarations.append(
                    {
                        "name": fuzzy_field,
                        "type": "fuzzyFieldType",
                        "multiValued": False,
                    }
                )
            else:
                payload_declarations.append(
                    {"name": fuzzy_field, "type": "fuzzyFieldType", "multiValued": True}
                )

        return {"add-field": payload_declarations}

    # @staticmethod
    # def all_in_one_field() -> dict[str, Any]:
    #     pass
