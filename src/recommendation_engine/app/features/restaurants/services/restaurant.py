from ..db.models import RestaurantModel
from ..dto.restaurants import RestaurantDto
from ....shared_kernel.database.clickhouse import get_session


class RestaurantService:
    @staticmethod
    def parse_all_restaurants(
        restaurants: list[RestaurantDto], lat: float, lon: float, city: str
    ):
        with get_session() as session:
            session.bulk_save_objects(
                [
                    RestaurantModel(**element.model_dump(), lat=lat, lon=lon, city=city)
                    for element in restaurants
                ]
            )
