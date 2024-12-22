from typing import Any
from ...menu.db import MenuModel
from ...comments.db import CommentsModel
from ...restaurants.db import RestaurantModel


class AggregateDomainsService:
    @staticmethod
    def retrieve_aggregate_data() -> list[dict[str, Any]]:
        pass
