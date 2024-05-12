from loguru import logger
from typing import Generator

from ...entity import BaseEntity
from ...request import RequestValue
from ...value_stack import EntityValueStack
from ...processor import Processor, SyncCallParams
from ..values.yemeksepeti import YemeksepetiCommentValue


class YemekSepetiComments(BaseEntity, Processor):
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
                            "created_at": "desc",
                            "has_dish": True,
                            "nextPageKey": "{next_page_key}"                            
                        }}
                    """,
        )
        self.comment_stack = EntityValueStack()

    def _iterate_over_comments(self) -> Generator[dict, None, None]:
        next_page_key = ""
        while True:
            request_template = (
                self.filter_and_search_payload.retrieve_formatted_request(
                    {"next_page_key": next_page_key}
                )
            )
            sync_call_params = SyncCallParams(**request_template)
            response = self.synchronized_call(sync_call_params)
            data = self._retrieve_json_from_response(response)

            if not data:
                break

            comments = data.get("data")
            next_page_key = data.get("pageKey", "")

            if not comments:
                break

            yield comments
            logger.info(
                f"Page was crawled. total crawled data is {len(self.comment_stack)}"
            )
            if not next_page_key:
                break

    @staticmethod
    def transform_unstructured_data(record_value: dict) -> YemeksepetiCommentValue:
        values = dict()
        values["comment_id"] = record_value.get("uuid")
        values["created_at"] = record_value.get("createdAt")
        values["updated_at"] = record_value.get("updatedAt")
        values["comment"] = record_value.get("text")
        values["reviewer_name"] = record_value.get("reviewerName")
        values["reviewer_id"] = record_value.get("reviewerId")
        values["rating"] = record_value.get("ratings")
        values["comment_like_count"] = record_value.get("likeCount")
        values["product_variation"] = record_value.get("productVariations")
        values["replies"] = record_value.get("replies")

        comment_value = YemeksepetiCommentValue(**values)
        return comment_value

    def process(
        self, process_limit: int | None = None
    ) -> list[YemeksepetiCommentValue]:
        for comment_list in self._iterate_over_comments():
            for comment in comment_list:
                comment = self.transform_unstructured_data(comment)
                self.comment_stack.add_value(comment)

            if process_limit is not None and len(self.comment_stack) >= process_limit:
                break

        return self.comment_stack.retrieve_values()
