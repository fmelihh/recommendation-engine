from ..dto.menu import MenuDto
from ..domain.entity.getir import GetirMenuValue
from ..domain.entity.yemeksepeti import YemeksepetiMenuValue


class MenuMapper:
    @staticmethod
    def yemeksepeti_menu_to_dto(value_object: YemeksepetiMenuValue) -> MenuDto:
        menu_dto = MenuDto(
            category=value_object.category,
            product_id=value_object.product_id,
            name=value_object.name,
            description=value_object.description,
            image_url=value_object.image_url,
            price=value_object.price.amount,
            price_currency=value_object.price.currency,
        )
        return menu_dto

    @staticmethod
    def getir_menu_to_dto(value_object: GetirMenuValue) -> MenuDto:
        menu_dto = MenuDto(
            category=value_object.category,
            product_id=value_object.product_id,
            name=value_object.name,
            description=value_object.description,
            image_url=value_object.image_url,
            price=value_object.price.amount,
            price_currency=value_object.price.currency,
        )
        return menu_dto
