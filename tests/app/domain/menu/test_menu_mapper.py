from src.recommendation_engine.app.features.menu.dto.menu import MenuDto
from src.recommendation_engine.app.features.menu.mappers.menu import (
    MenuMapper,
)
from src.recommendation_engine.app.features.menu.domain.values.getir import (
    GetirMenuValue,
)
from src.recommendation_engine.app.features.menu.domain.values.yemeksepeti.menu import (
    YemeksepetiMenuValue,
)


def test_getir_mapper():
    getir_domain_value = GetirMenuValue(
        category="a",
        product_id="a",
        name="a",
        price="31",
        description="a",
        image_url="https://a.com",
        full_screen_image_url="https://a.com",
        is_available=False,
    )
    res = MenuMapper.getir_menu_to_dto(value_object=getir_domain_value)
    assert isinstance(res, MenuDto)


def test_yemeksepeti_mapper():
    yemeksepeti_domain_value = YemeksepetiMenuValue(
        category="a",
        product_id="a",
        name="a",
        price=3,
        description="a",
        image_url="https://a.com",
    )

    res = MenuMapper.yemeksepeti_menu_to_dto(value_object=yemeksepeti_domain_value)
    assert isinstance(res, MenuDto)
