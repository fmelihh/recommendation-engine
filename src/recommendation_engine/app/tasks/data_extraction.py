import celery
from celery.app.task import Task
from celery.schedules import crontab

from ..shared_kernel.scheduler.celery_app import celery_application


class DataExtractionTask(Task):
    __name__ = "DataExtractionTask"

    def run(self, *args, **kwargs):
        from .menu import MenuTask
        from .comments import CommentTask
        from .restaurant import RestaurantTask

        menu_task = MenuTask()
        comment_task = CommentTask()
        restaurant_task = RestaurantTask()

        celery.chain(restaurant_task.s(), menu_task.s(), comment_task.s()).apply_async()


celery_application.register_task(DataExtractionTask)
celery_application.conf.beat_schedule[str(DataExtractionTask.__name__)] = {
    "task": str(DataExtractionTask.__module__),
    "schedule": crontab(hour="12", minute="30"),
    "options": {"queue": "periodic"},
}
