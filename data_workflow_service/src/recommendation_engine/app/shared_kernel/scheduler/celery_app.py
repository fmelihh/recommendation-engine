import os
from celery import Celery

celery_application = Celery("app")
celery_application.conf.timezone = os.getenv("CELERY_TIMEZONE")
celery_application.conf.broker_url = os.getenv("REDIS_HOST")
celery_application.conf.result_backend = os.getenv("REDIS_PORT")

__all__ = ["celery_application"]
