from celery import Celery

celery_application = Celery("app")
celery_application.conf.timezone = "UTC"
celery_application.conf.broker_url = "redis://localhost:6379/0"
celery_application.conf.result_backend = "redis://localhost:6379/0"

__all__ = ["celery_application"]
