from ..dto.restaurants import RestaurantDto
from ..domain.entity.getir import GetirRestaurantValue
from ..domain.entity.yemek_sepeti import YemeksepetiRestaurantValue


class RestaurantMapper:
    @staticmethod
    def yemeksepeti_restaurant_to_dto(
        value_object: YemeksepetiRestaurantValue,
    ) -> RestaurantDto:
        restaurant_dto = RestaurantDto(
            restaurant_slug=value_object.url_slug,
            restaurant_id=value_object.restaurant_id,
            name=value_object.name,
            rating=value_object.rating,
            image_url=None,
            review_number=value_object.review_number,
            order_amount=value_object.minimum_order_amount.amount,
            order_amount_currency=value_object.minimum_order_amount.currency,
            delivery_fee=value_object.minimum_delivery_fee.amount,
            delivery_fee_currency=value_object.minimum_delivery_fee.currency,
            delivery_time=value_object.minimum_delivery_time,
            loyalty_percentage_amount=value_object.loyalty_percentage_amount,
        )
        return restaurant_dto

    @staticmethod
    def getir_restaurant_to_dto(value_object: GetirRestaurantValue) -> RestaurantDto:
        restaurant_dto = RestaurantDto(
            restaurant_slug=value_object.slug,
            restaurant_id=value_object.id,
            name=value_object.name,
            rating=value_object.rating_point,
            image_url=value_object.image_url,
            review_number=value_object.rating_count.count,
            delivery_fee=value_object.delivery_fee.amount,
            delivery_fee_currency=value_object.delivery_fee.currency,
            delivery_time=value_object.estimated_delivery_time.unit,
        )
        return restaurant_dto
