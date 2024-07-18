from celery.app.task import Task


from ..shared_kernel.scheduler.celery_app import celery_application
from ..features.menu.services import MenuExtractorService, MenuService


class MenuTask(Task):
    __name__ = "MenuTask"

    def run(self, *args, **kwargs):
        menu_service = MenuService()
        menu_extractor = MenuExtractorService(**kwargs)

        restaurant_list = menu_extractor.crawl()
        menu_service.parse_all_menus(restaurant_list)


celery_application.register_task(MenuTask)
