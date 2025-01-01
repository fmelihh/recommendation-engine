from .base import AbstractSolr


class SolrQuery(AbstractSolr):
    def __init__(self):
        super().__init__()

    def search(
        self,
        page: int,
        page_size: int,
        search_text: str,
        fuzzy_search_text: str,
        lat: str | None = None,
        lon: str | None = None,
    ):
        query = """
            provider:{search_text}^2 OR
            restaurant_name:{search_text}^10 OR
            restaurant_city:{search_text}^2 OR
            comments:{search_text}^3.5 OR
            product_categories:{search_text}^3.5 OR
            product_names:{search_text}^4.5
            product_description:{search_text}^3.5 OR
            
            provider:{fuzzy_search_text}^1 OR
            restaurant_name:{fuzzy_search_text}^5 OR
            restaurant_city:{fuzzy_search_text}^1 OR
            comments:{fuzzy_search_text}^1.7 OR
            product_categories:{fuzzy_search_text}^1.7 OR
            product_names:{fuzzy_search_text}^2.3
            product_description:{fuzzy_search_text}^1.7
        """
        start = page * page_size
        result = self.solr_client.search(
            "",
            start=start,
            rows=page_size,
            defType="dismax",
            fl="*, score",
            bf="sum(mul(restaurant_rate,0.5),mul(review_number,0.3),mul(comment_avg_rating,0.5))",
            sort="score desc",
            **{
                "q.alt": query.format(
                    search_text=search_text,
                    fuzzy_search_text=fuzzy_search_text,
                ),
            },
        )

        return result
