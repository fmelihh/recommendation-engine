import os
import json
from celery.app.task import Task
from celery.schedules import crontab

from ..shared_kernel.domain_providers import Providers
from ..shared_kernel.scheduler.celery_app import celery_application
from ..features.restaurants.services import (
    RestaurantService,
    RestaurantExtractorService,
)


class RestaurantTask(Task):
    __name__ = "RestaurantTask"

    def run(self, *args, **kwargs):
        cities = json.load(
            open(f"{os.getcwd()}/static/{os.getenv('CITIES_JSON')}", "r")
        )

        for city in cities:
            for provider in Providers:

                lat = float(city["latitude"])
                lon = float(city["longitude"])

                restaurant_service = RestaurantService()
                restaurant_extractor = RestaurantExtractorService(
                    provider_type=provider, lat=lat, lon=lon
                )

                restaurant_list = restaurant_extractor.crawl()
                if len(restaurant_list) > 0:
                    restaurant_service.parse_all_restaurants(
                        provider=provider.value,
                        restaurants=restaurant_list,
                        lat=lat,
                        lon=lon,
                        city=city["name"].upper(),
                    )


celery_application.register_task(RestaurantTask)

celery_application.conf.beat_schedule[str(RestaurantTask.__name__)] = {
    "task": str(RestaurantTask.__module__),
    "schedule": crontab(hour="12", minute="30"),
    "options": {"queue": "periodic"},
}
