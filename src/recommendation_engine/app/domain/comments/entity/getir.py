from loguru import logger
from typing import Generator

from ...entity import BaseEntity
from ...request import RequestValue
from ...value_stack import EntityValueStack
from ..values.getir import GetirCommentValue
from ...processor import Processor, SyncCallParams


class GetirComments(BaseEntity, Processor):
    HEADERS = {
        "authority": "food-client-api-gateway.getirapi.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,tr;q=0.8",
        "content-type": "application/json",
        "language": "tr",
        "origin": "https://getir.com",
        "referer": "https://getir.com/",
    }

    def __init__(self, restaurant_id: str):
        super().__init__()
        self.restaurant_id = restaurant_id
        self.filter_and_search_payload = RequestValue(
            url=f"https://food-client-api-gateway.getirapi.com/restaurants/{self.restaurant_id}/reviews",
            method="GET",
            template_loc="params",
            headers=self.HEADERS,
            template="""
                {{
                    "skip": {skip}
                }}
            """,
        )
        self.comment_stack = EntityValueStack()

    def _iterate_over_comments(self) -> Generator[dict, None, None]:
        skip = 0
        while 1:
            request_template = (
                self.filter_and_search_payload.retrieve_formatted_request(
                    {"skip": skip}
                )
            )
            sync_call_params = SyncCallParams(**request_template)
            response = self.synchronized_call(sync_call_params)
            data = self._retrieve_json_from_response(response)

            if not data:
                break

            comments = data.get("data", {}).get("reviews", [])

            if not comments:
                break

            yield comments
            logger.info(
                f"page {skip} was crawled. total crawled data is {len(self.comment_stack)}"
            )

            skip += 10


    @staticmethod
    def transform_unstructured_data(record_value: dict) -> GetirCommentValue:
        values = dict()
        values["review_id"] = record_value.get("uuid")
        values["date_text"] = record_value.get("createdAt")
        values["restaurant_reply"] = record_value.get("text")
        values["restaurant_rating"] = record_value.get("restaurantRating")
        values["restaurant_comment"] = record_value.get("restaurantComment")
        values["chips_rating"] = record_value.get("chipsRating")

        comment_value = GetirCommentValue(**values)
        return comment_value

    def process(self, process_limit: int | None = None) -> list[GetirCommentValue]:
        for comment_list in self._iterate_over_comments():
            for comment in comment_list:
                comment = self.transform_unstructured_data(comment)
                self.comment_stack.add_value(comment)

            if process_limit is not None and len(self.comment_stack) >= process_limit:
                break

        return self.comment_stack.retrieve_values()
