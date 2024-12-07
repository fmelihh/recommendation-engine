from celery.app.task import Task
from celery.schedules import crontab

from ..shared_kernel.scheduler.celery_app import celery_application
from ..features.comments.services import (
    CommentService,
    CommentsExtractorService,
)
from ..shared_kernel.domain_providers import Providers
from ..features.restaurants.services import RestaurantService


class CommentTask(Task):
    __name__ = "CommentTask"

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
                    comment_restaurant_id = (
                        restaurant.restaurant_slug.split("-")[-1]
                        if provider == Providers.YEMEK_SEPETI
                        else restaurant.restaurant_id
                    )
                    comment_service = CommentService()
                    comment_extractor = CommentsExtractorService(
                        provider_type=provider, restaurant_id=comment_restaurant_id
                    )

                    comment_list = comment_extractor.crawl()
                    if len(comment_list) > 0:
                        comment_service.parse_all_comments(
                            restaurant_id=restaurant.restaurant_id,
                            provider=provider.value,
                            comments=comment_list,
                        )

                counter += 1


celery_application.register_task(CommentTask)


celery_application.conf.beat_schedule[str(CommentTask.__name__)] = {
    "task": str(CommentTask.__module__),
    "schedule": crontab(hour="12", minute="30"),
    "options": {"queue": "periodic"},
}
