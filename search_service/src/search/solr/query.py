from .base import AbstractSolr


class SolrQuery(AbstractSolr):
    def __init__(self):
        super().__init__()

    def search(self):
        pass
