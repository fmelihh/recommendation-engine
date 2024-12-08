from ..db.model import CommentsModel
from ..dto.comment import CommentDto
from ....shared_kernel.generator import HashGenerator
from ....shared_kernel.database.clickhouse import get_session


class CommentService:
    @staticmethod
    def parse_all_comments(
        restaurant_id: str, provider: str, comments: list[CommentDto]
    ):
        with get_session() as session:
            session.bulk_save_objects(
                [
                    CommentsModel(
                        restaurant_id=restaurant_id,
                        provider=provider,
                        **comments[idx].model_dump(exclude_none=True),
                        id=HashGenerator.generate_unique_hash(
                            [
                                provider,
                                restaurant_id,
                                comments[idx].comment_id,
                            ]
                        )
                    )
                    for idx in range(len(comments))
                ]
            )
