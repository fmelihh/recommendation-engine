from typing import Any

from .base import AbstractSolr


class SolrQuery(AbstractSolr):
    def __init__(self):
        super().__init__()

    def search(
        self,
        page: int,
        page_size: int,
        search_text: str,
        search_text_and: str,
        search_text_or: str,
    ):
        query = """
            provider:{search_text}^2 OR
            restaurant_name:{search_text}^10 OR
            restaurant_city:{search_text}^2 OR
            comments:{search_text}^3.5 OR
            product_categories:{search_text}^3.5 OR
            product_names:{search_text}^4.5
            product_description:{search_text}^3.5 OR
            
            provider:{search_text_and}^2 OR
            restaurant_name:{search_text_and}^10 OR
            restaurant_city:{search_text_and}^2 OR
            comments:{search_text_and}^3.5 OR
            product_categories:{search_text_and}^3.5 OR
            product_names:{search_text_and}^4.5
            product_description:{search_text_and}^3.5 OR
            
            provider:{search_text_or}^0.5 OR
            restaurant_name:{search_text_or}^3.5 OR
            restaurant_city:{search_text_or}^0.5 OR
            comments:{search_text_or}^0.3 OR
            product_categories:{search_text_or}^0.3 OR
            product_names:{search_text_or}^0.3
            product_description:{search_text_or}^0.3
        """
        start = page * page_size
        result = self.solr_client.search(
            "",
            start=start,
            rows=page_size,
            defType="dismax",
            fl="*, score",
            bf="sum(mul(scale(restaurant_rate,1,20),0.5),mul(scale(review_number,1,20),0.3),mul(scale(comment_avg_rating,1,20),0.5))",
            sort="score desc",
            **{
                "q.alt": query.format(
                    search_text=search_text,
                    search_text_and=search_text_and,
                    search_text_or=search_text_or,
                ),
            },
        )

        return list(result.docs)

    def get_restaurants_with_id(
        self, restaurant_ids: list[str]
    ) -> list[dict[str, Any]]:
        results = []
        for restaurant_id in restaurant_ids:
            result = self.solr_client.search(
                "",
                start=0,
                rows=1,
                defType="dismax",
                fl="*, score",
                sort="score desc",
                **{
                    "q.alt": f'restaurant_id:"{restaurant_id}"',
                },
            )
            if len(result.docs) == 0:
                continue

            results.append(result.docs[0])

        return results
