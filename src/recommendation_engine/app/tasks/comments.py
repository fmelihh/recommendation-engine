from celery.app.task import Task

from ..shared_kernel.scheduler.celery_app import celery_application
from ..features.comments.services import (
    CommentService,
    CommentsExtractorService,
)


class CommentTask(Task):
    __name__ = "CommentTask"

    def run(self, *args, **kwargs):
        comment_service = CommentService()
        comment_extractor = CommentsExtractorService(**kwargs)

        comment_list = comment_extractor.crawl()
        comment_service.parse_all_comments(comment_list)


celery_application.register_task(CommentTask)
