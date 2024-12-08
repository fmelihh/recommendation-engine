from typing import Any
from pysolr import Solr


class SolrQuery:
    def __init__(self):
        self._client = Solr(
            url="http://localhost:8983/solr/recommendation-engine",
        )
        self._client.ping()

    @staticmethod
    def _format_query_response(result: dict):
        return {
            k: v[0] if ((type(v) is list) and (len(v) > 0)) else v
            for k, v in result.items()
            if not k.startswith("_") and not k.endswith("_")
        }

    def search(self, text: str, page: int, total_page: int):
        page = page * total_page
        search_obj = self._client.search(
            "",
            start=page,
            rows=total_page,
            defType="dismax",
            fl="*, score",
            # bf="mul(rating,0.5)",
            sort="score desc",
            **{
                "q.alt": f"""
                   name: {text}^5 OR
                   provider: {text}^2 OR
                   city: {text}^1 OR
                   
                   name: ({text}~1)^1.5 OR
                   provider: ({text}~1)^1 OR
                   city: ({text}~1)^0.5 OR
                   
                   name: ({text}~2)^0.75 OR
                   provider: ({text}~2)^0.5 OR
                   city: ({text}~2)^0.1 OR
                """,
            },
        )

        return {
            "page": page,
            "total_page": total_page,
            "data": [self._format_query_response(record) for record in search_obj],
        }

    def data_upload(self, data: list[dict[str, Any]]):
        self._client.add(data)
        self._client.commit()
        self._client.optimize()
