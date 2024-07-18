from celery.app.task import Task

from ..shared_kernel.scheduler.celery_app import celery_application


class CommentTask(Task):
    __name__ = "CommentTask"

    def run(self, *args, **kwargs):
        pass


celery_application.register_task(CommentTask)
