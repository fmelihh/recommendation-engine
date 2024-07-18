from celery.app.task import Task

from ..shared_kernel.scheduler.celery_app import celery_application
from ..features.restaurants.services import (
    RestaurantService,
    RestaurantExtractorService,
)


class RestaurantTask(Task):
    __name__ = "RestaurantTask"

    def run(self, *args, **kwargs):
        restaurant_service = RestaurantService()
        restaurant_extractor = RestaurantExtractorService(
            lat=kwargs["lat"], lon=kwargs["lon"]
        )

        restaurant_list = restaurant_extractor.crawl()
        restaurant_service.parse_all_restaurants(restaurant_list)


celery_application.register_task(RestaurantTask)
