from celery.app.task import Task
from celery.schedules import crontab

from ..services.upload import UploadService
from .celery_app import celery_application


class DataFetchTask(Task):
    __name__ = "DataFetchTask"

    def run(self, *args, **kwargs):
        service = UploadService()
        fetch_data_generator = service.fetch_data()

        first_data = next(fetch_data_generator)
        service.solr_collection_migration()
        service.parse_data_to_solr(data=first_data, reindex=True)

        for next_data in fetch_data_generator:
            service.parse_data_to_solr(next_data, reindex=False)


celery_application.register_task(DataFetchTask)

celery_application.conf.beat_schedule[str(DataFetchTask.__name__)] = {
    "task": str(DataFetchTask.__module__),
    "schedule": crontab(hour="12", minute="30"),
    "options": {"queue": "periodic"},
}
