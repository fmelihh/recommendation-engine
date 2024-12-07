from celery.app.task import Task
from celery.schedules import crontab

from ..shared_kernel.domain_providers import Providers
from ..features.restaurants.services import RestaurantService
from ..shared_kernel.scheduler.celery_app import celery_application
from ..features.menu.services import MenuExtractorService, MenuService


class MenuTask(Task):
    __name__ = "MenuTask"

    def run(self, *args, **kwargs):
        for provider in Providers:
            counter = 0
            while True:
                restaurants = RestaurantService.retrieve_restaurants_with_pagination(
                    provider=provider.value, start=counter, page=100
                )
                if len(restaurants) == 0:
                    break

                for restaurant in restaurants:
                    menu_service = MenuService()
                    menu_extractor = MenuExtractorService(
                        provider_type=provider.value,
                        lat=restaurant.lat,
                        lon=restaurant.lon,
                        restaurant_slug=restaurant.restaurant_slug,
                        restaurant_id=restaurant.restaurant_id,
                    )

                    menu_list = menu_extractor.crawl()

                    if len(menu_list) > 0:
                        menu_service.parse_all_menus(
                            restaurant_id=restaurant.restaurant_id,
                            provider=provider.value,
                            menus=menu_list,
                        )

                counter += 1


celery_application.register_task(MenuTask)

celery_application.conf.beat_schedule[str(MenuTask.__name__)] = {
    "task": str(MenuTask.__module__),
    "schedule": crontab(hour="12", minute="30"),
    "options": {"queue": "periodic"},
}