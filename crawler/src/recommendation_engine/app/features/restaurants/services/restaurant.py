from ..db import RestaurantModel
from ..dto.restaurants import RestaurantDto
from ....shared_kernel.database.clickhouse import get_session
from ....shared_kernel.generator import HashGenerator


class RestaurantService:
    @staticmethod
    def parse_all_restaurants(
        provider: str,
        restaurants: list[RestaurantDto],
        lat: float,
        lon: float,
        city: str,
    ):
        with get_session() as session:
            session.bulk_save_objects(
                [
                    RestaurantModel(
                        lat=lat,
                        lon=lon,
                        city=city,
                        provider=provider,
                        **restaurants[idx].model_dump(),
                        id=HashGenerator.generate_unique_hash(
                            [
                                provider,
                                restaurants[idx].restaurant_id,
                                restaurants[idx].restaurant_slug,
                            ]
                        )
                    )
                    for idx in range(len(restaurants))
                ]
            )

    @staticmethod
    def retrieve_restaurants_with_pagination(
        provider: str, start: int = 0, page: int = 10
    ) -> list[RestaurantDto]:
        with get_session() as session:
            restaurants = (
                session.query(RestaurantModel)
                .filter(RestaurantModel.provider == provider)
                .offset(page * start)
                .limit(page)
                .all()
            )

            return [RestaurantDto(**restaurant.__dict__) for restaurant in restaurants]
