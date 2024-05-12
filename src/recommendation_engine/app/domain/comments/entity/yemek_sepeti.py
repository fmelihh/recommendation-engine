from loguru import logger
from typing import Generator

from ...entity import BaseEntity
from ...processor import Processor, SyncCallParams
from ..values import CommentValue, RequestValue, CommentStack


class YemekSepeti(BaseEntity, Processor):
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.yemeksepeti.com",
        "perseus-client-id": "1715372289643.728421729131829214.jbyk0nystp",
        "perseus-session-id": "1715372289643.707748580212862372.cbhwjz0m2c",
        "priority": "u=1, i",
        "referer": "https://www.yemeksepeti.com/",
        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "x-pd-language-id": "2",
        "Cookie": "__cf_bm=jQUwOPufx1Ill_YuUW9Qk55HtJW7QcqU11VsXXMrZqw-1715501543-1.0.1.1-.ArnmwCY3ev_YC7_4SL8QTxNJjYAskuVnyfJJDFF3YsJAndaH3JDLtVGiFqwwD2D4HbfFY8MKynONUowZ2AIem.COi9YFpiC6bCoAVtZobM",
    }

    def __init__(self, restaurant_id: str):
        super().__init__()
        self.restaurant_id = restaurant_id
        self.filter_and_search_payload = RequestValue(
            url=f"https://reviews-api-tr.fd-api.com/reviews/vendor/{self.restaurant_id}",
            method="GET",
            template_loc="params",
            headers=self.HEADERS,
            template="""
                        {{
                            "global_entity_id": "YS_TR",
                            "limit": 30,
                            "created_at": "desc"
                            "has_dish": True
                            "nextPageKey": {page_key}                            
                        }}
                    """,
        )
        self.comment_stack = CommentStack()

    def process(self, process_limit: int | None = None) -> list[CommentValue]:
        pass
