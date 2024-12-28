from .base import AbstractSolr


class SolrQuery(AbstractSolr):
    def __init__(self):
        super().__init__()

    def search(self):
        pass

    # @staticmethod
    # def _format_query_response(result: dict):
    #     return {
    #         k: v[0] if ((type(v) is list) and (len(v) > 0)) else v
    #         for k, v in result.items()
    #         if not k.startswith("_") and not k.endswith("_")
    #     }
