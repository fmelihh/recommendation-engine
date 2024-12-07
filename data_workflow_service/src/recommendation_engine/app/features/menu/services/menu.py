from ..db import MenuModel
from ..dto.menu import MenuDto
from ....shared_kernel.generator import HashGenerator
from ....shared_kernel.database.clickhouse import get_session


class MenuService:
    @staticmethod
    def parse_all_menus(restaurant_id: str, provider: str, menus: list[MenuDto]):
        with get_session() as session:
            session.bulk_save_objects(
                [
                    MenuModel(
                        restaurant_id=restaurant_id,
                        provider=provider,
                        id=HashGenerator.generate_unique_hash(
                            [
                                provider,
                                restaurant_id,
                                menus[idx].product_id,
                            ]
                        ),
                        **menus[idx].model_dump()
                    )
                    for idx in range(len(menus))
                ]
            )
