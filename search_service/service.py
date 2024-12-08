import io
import numpy as np
import pandas as pd
from typing import Generator
from solr import SolrQuery


class SearchService:
    def __init__(self):
        self._solr_query = None

    @property
    def solr_query(self) -> SolrQuery:
        if self._solr_query is None:
            self._solr_query = SolrQuery()
        return self._solr_query

    @staticmethod
    def _convert_bytes_to_dataframe(
        content: bytes, content_type: str
    ) -> Generator[pd.DataFrame, None, None]:
        if content_type not in ("text/csv",):
            raise ValueError("unsupported file type")

        buffer = io.BytesIO(content)
        df = pd.read_csv(buffer, chunksize=300, sep=",", index_col=0)

        for chunk_df in df:
            yield chunk_df.replace({np.nan: None})

        buffer.close()

    def search_restaurant(self, text: str, page: int, total_page: int):
        return self.solr_query.search(
            text=text,
            page=page,
            total_page=total_page,
        )

    def data_upload(self, content: bytes, content_type: str):
        for chunk_df in self._convert_bytes_to_dataframe(
            content=content, content_type=content_type
        ):
            data = chunk_df.to_dict(orient="records")
            self.solr_query.data_upload(data=data)
