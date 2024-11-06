from ..db.models import RestaurantModel
from ..dto.restaurants import RestaurantDto
from ....shared_kernel.database.clickhouse import get_session
from ....shared_kernel.generator import HashGenerator


class RestaurantService:
    @staticmethod
    def parse_all_restaurants(
        restaurants: list[RestaurantDto], lat: float, lon: float, city: str
    ):
        with get_session() as session:
            session.bulk_save_objects(
                [
                    RestaurantModel(
                        lat=lat,
                        lon=lon,
                        city=city,
                        **restaurants[idx].model_dump(),
                        id=HashGenerator.generate_unique_hash(
                            [
                                restaurants[idx].restaurant_id,
                                restaurants[idx].restaurant_slug,
                            ]
                        )
                    )
                    for idx in range(len(restaurants))
                ]
            )
