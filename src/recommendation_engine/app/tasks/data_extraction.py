from celery.app.task import Task
from celery.schedules import crontab

from ..shared_kernel.scheduler.celery_app import celery_application


class DataExtractionTask(Task):
    __name__ = "DataExtractionTask"

    def run(self, *args, **kwargs):
        pass


celery_application.register_task(DataExtractionTask)
celery_application.conf.beat_schedule[str(DataExtractionTask.__name__)] = {
    "task": str(DataExtractionTask.__module__),
    "schedule": crontab(hour="12", minute="30"),
    "options": {"queue": "periodic"},
}
