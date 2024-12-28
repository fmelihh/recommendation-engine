from typing import Any

from .base import AbstractSolr


class SolrSchema(AbstractSolr):
    def __init__(self):
        super().__init__()

    @staticmethod
    def fuzzy_search_field_type() -> dict[str, Any]:
        return {
            "add-field-type": {
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
        }

    @staticmethod
    def search_fields() -> dict[str, Any]:
        multivalued_fields = [
            "comments",
            "product_categories",
            "product_names",
            "product_description",
        ]

        str_fields = ["restaurant_id"]
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
        float_fields = ["restaurant_rate", "lat", "lon", "comment_avg_rating"]

        payload_declarations = []
        for str_field in str_fields:
            payload_declarations.append(
                {"name": str_field, "type": "string", "multiValued": False}
            )
        for int_field in int_fields:
            payload_declarations.append(
                {"name": int_field, "type": "int", "multiValued": False}
            )
        for float_field in float_fields:
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
