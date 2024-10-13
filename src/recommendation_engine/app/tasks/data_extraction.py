import os
import json
import celery
from loguru import logger
from celery.app.task import Task
from celery.schedules import crontab

from ..shared_kernel.domain_providers import Providers
from ..shared_kernel.scheduler.celery_app import celery_application


class DataExtractionTask(Task):
    __name__ = "DataExtractionTask"

    def run(self, *args, **kwargs):
        from .menu import MenuTask
        from .comments import CommentTask
        from .restaurant import RestaurantTask

        batch_size = 3
        cities = json.load(open(f"{os.getcwd()}/static/cities.json", "r"))

        for i in range(0, len(cities), batch_size):
            for provider in Providers:
                batch = cities[i : i + batch_size]
                tasks = []

                for city in batch:
                    restaurant_task = RestaurantTask()
                    tasks.append(
                        celery.chain(
                            restaurant_task.s(
                                provider=provider, lat=city["lat"], lon=city["lon"]
                            ),
                            MenuTask().s(),
                            CommentTask().s(),
                        )
                    )
                celery.group(*tasks).apply_async()
                logger.info("Data Extraction Task queue started.")


celery_application.register_task(DataExtractionTask)
celery_application.conf.beat_schedule[str(DataExtractionTask.__name__)] = {
    "task": str(DataExtractionTask.__module__),
    "schedule": crontab(hour="12", minute="30"),
    "options": {"queue": "periodic"},
}
