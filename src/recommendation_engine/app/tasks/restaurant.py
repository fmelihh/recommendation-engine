from celery.app.task import Task

from ..shared_kernel.scheduler.celery_app import celery_application


class RestaurantTask(Task):
    __name__ = "RestaurantTask"

    def run(self, *args, **kwargs):
        pass


celery_application.register_task(RestaurantTask)
