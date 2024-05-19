from loguru import logger
from typing import Generator

from ..values import GeoValue
from ...entity import BaseEntity
from ...processor import Processor
from ...request import RequestValue
from ...processor import SyncCallParams
from ...value_stack import EntityValueStack
from ..values.yemeksepeti import YemeksepetiRestaurantValue


class YemeksepetiRestaurants(BaseEntity, Processor):
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.5",
        "app-version": "MICROFRONT.24.19.21",
        "authorization": "",
        "content-type": "application/json;charset=UTF-8",
        "dps-session-id": "eyJzZXNzaW9uX2lkIjoiZGIzMzlhY2YxNzAwODI3MDY4YTI4OWRlMWRlZmVhNzIiLCJwZXJzZXVzX2lkIjoiMTcxNTUwMTA0ODc1MC42MTE0MzU1MDgwNDM4Nzg3MjUuemprenQ1ZWJ1NCIsInRpbWVzdGFtcCI6MTcxNjExNjQ3MH0=",
        "origin": "https://www.yemeksepeti.com",
        "perseus-client-id": "1715501048750.611435508043878725.zjkzt5ebu4, 1715501048750.611435508043878725.zjkzt5ebu4",
        "perseus-session-id": "1716116458577.775017342463159347.34gzo10s2c, 1716116458577.775017342463159347.34gzo10s2c",
        "platform": "web",
        "priority": "u=1, i",
        "referer": "https://www.yemeksepeti.com/",
        "request-id": "092b0814-6b8e-4b3b-abc3-7f4cbee7bf3b",
        "sec-ch-ua": '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "x-fp-api-key": "volo",
        "Cookie": "__cf_bm=nKKuwM8EMITFdJCg1MVwyIw9KnvdzGemJKOWER29eig-1716126007-1.0.1.1-B6gG2WIMSFWXQv6ymSUHEGlPE3pdwrbktwSAJHu0eutazV.9rOxFNf2deB2Pya5op_f1EQDvc1zmGbh_xqFiNR1PS2pmEPj7z.4Ck82bRGY; _pxhd=9HaOfVx/NM11ec4-HH0ZeHwXi9GRhgt23C4fbGHA5QEr-Q0Aqfjbck6tF1boUMPCEHlW8CWMOichWaTfho-S2w==:d8rqC0l1UGGUr2GfGG2xp9k58RgZwM7EiXxcjhWsu0MSrciyWuh0ME24dvtYo9w3JfjIlpNQoOE/KdQRaHcXqXIzizmsnFtOBzKkbW8X8cg=",
    }

    def __init__(self, geo_value: GeoValue) -> None:
        super().__init__()
        self.geo_value = geo_value
        self.filter_and_search_payload = RequestValue(
            url="https://tr.fd-api.com/rlp-service/query",
            method="POST",
            template_loc="body",
            headers=self.HEADERS,
            template="""
                {{
                "query": '''\nquery getOrganicListing(\n        $input: RLPInput!\n        $includeCarousels: Boolean!\n        $includeSwimlanes: Boolean!\n        $includeJoker: Boolean!\n        $includeDynamicSearchbarConfig: Boolean!\n    ) {{\n        rlp(params: $input) {{\n            organic_listing {{\n                views {{\n                    returned_count\n                    available_count\n                    aggregations {{\n                        ...Aggregations\n                    }}\n                    items {{\n                        ...Vendor\n                    }}\n                    events {{\n                        ...VendorEvent\n                    }}\n                    # ======================= EXCLUDED FIELDS ======================== #\n                    #banner: String!\n                    #missing_vendor_reasons: Map\n                    #partner: OrganicListingPartner\n                    #tags: Map!\n                }}\n            }}\n\n            carousels @include(if: $includeCarousels) {{\n                ...Carousels\n            }}\n\n            swimlanes @include(if: $includeSwimlanes) {{\n                ...SwimlaneList\n            }}\n\n            joker_offers @include(if: $includeJoker) {{\n                ...JokerOffer\n            }}\n\n            dynamic_searchbar_config\n                @include(if: $includeDynamicSearchbarConfig) {{\n                ...DynamicSearchbarConfig\n            }}\n\n            errors {{\n                organic_listing\n                swimlanes\n                joker_offers\n                dynamic_searchbar_config\n            }}\n        }}\n    }}\n\n    fragment VendorEvent on VendorEvent {{\n        id\n        messages\n    }}\n\n    fragment Aggregations on OrganicListingAggregation {{\n        cuisines {{\n            ...AggregateCharacteristicFields\n        }}\n        food_characteristics {{\n            ...AggregateCharacteristicFields\n        }}\n        quick_filters {{\n            ...AggregateCharacteristicFields\n        }}\n        discount_labels {{\n            title\n            count\n        }}\n        delivery_providers {{\n            id\n            count\n        }}\n        partners {{\n            id\n            title\n            count\n            image_url\n            logo_url\n        }}\n        payment_types {{\n            id\n            title\n            count\n            highlighted\n        }}\n        close_reasons #(Diff structure) need to test!\n\n        # ======================= EXCLUDED FIELDS ======================== #\n        #events: [VendorEvent]!   On PARENT LEVEL\n        #banner: String!\n        #discounts: [OrganicListingDiscount]!\n        #food_characteristics_types: Map!\n    }}\n\n    fragment AggregateCharacteristicFields on OrganicListingAggregate {{\n        id\n        title\n        count\n    }}\n\n    fragment VendorMetadata on VendorMetadata {{\n        available_in\n        timezone\n        close_reasons\n        is_delivery_available\n        is_pickup_available\n        is_flood_feature_closed\n        is_temporary_closed\n        has_discount\n        events {{\n            ...VendorEvent\n        }}\n        # ======================= EXCLUDED FIELDS ======================== #\n        # name\n        # tags\n        # actions\n    }}\n\n    fragment Vendor on Vendor {{\n        id\n        code\n        budget\n        characteristics {{\n            cuisines {{\n                id\n                name\n                url_key\n            }}\n            food_characteristics {{\n                id\n                name\n            }}\n            primary_cuisine {{\n                id\n                name\n                url_key\n            }}\n        }}\n        accepts_instructions\n        delivery_provider\n        customer_type\n        is_active\n        is_preorder_enabled\n        is_best_in_city\n        tag\n        name\n        rating\n        review_number\n        address_line2\n        latitude\n        longitude\n        minimum_order_amount\n        minimum_delivery_fee\n        minimum_delivery_time\n        original_delivery_fee\n        delivery_fee_delta\n        free_delivery_label\n        minimum_pickup_time\n        is_vat_visible\n        is_vat_included_in_product_price\n        hero_listing_image\n        distance\n        has_delivery_provider\n        loyalty_program_enabled\n        loyalty_percentage_amount\n        vertical\n        is_premium\n        ncr_pricing_model\n        ncr_token\n        preorder_time_offset\n        partner_ids\n        metadata {{\n            ...VendorMetadata\n        }}\n        tags {{\n            code\n            text\n            origin\n            label_metadata {{\n                panda_pro {{\n                    is_pro\n                    type\n                    is_applicable\n                }}\n            }}\n        }}\n        tile {{\n            type\n            primary_tags {{\n                ...ElementGroup\n            }}\n            secondary_tags {{\n                ...ElementGroup\n            }}\n            vendor_info {{\n                ...ElementGroup\n            }}\n        }}\n        chain {{\n            code\n            name\n        }}\n        discounts_info {{\n            id\n            value\n        }}\n        location_event {{\n            id\n            message\n            tags\n            type\n            value\n            name\n        }}\n        favorite_data {{\n            favorited_on\n        }}\n        url_key\n        minimum_basket_value_discount {{\n            delivery_discount\n            is_free_delivery\n            threshold\n            is_pro\n            total_delivery_fee\n        }}\n\n        # ======================= EXCLUDED FIELDS ======================== #\n        # schedules          Vendor info from rdp\n        # specialDays        Vendor info from rdp\n        # web_path           Share on rdp\n        # customer_phone     Vendor contact on verticals\n        # budget             Search domain model\n        # primary_cuisine_id Search domain model & Redundant\n        # characteristics    Redundant information\n        # vertical_segment   Catering\n        # vertical_type_ids  Megamarts\n        # tag\n        # redirection_url\n        # maximum_express_order_amount\n        # is_vat_included_in_product_price\n        # allergens_link\n        # is_best_in_city\n        # accepts_instructions\n    }}\n\n    # ======================= Not Exist FIELDS in the Schema ======================== #\n    #menus                               RDP\n    #toppings                            RDP\n    #products                            Search\n    #search_metadata                     Search\n    #review_with_comment_number          DINE_IN\n    #is_vat_included & other vat fields  Cart\n    #trade_register_number               Checkout - payment\n    #time_picker                         Megamart\n    #imprint                             Shops\n    #topic_ratings                       Vendor Scoring/reviews Verticals\n\n    \n    \n    fragment CarouselItem on Campaign {{\n        campaign_id\n        active\n        ranking\n        title\n        subtitle\n        info\n        expedition_types\n        vertical_types\n        image_small\n        image_medium\n        image_large\n        image_small_desktop\n        image_large_desktop\n        url_key\n        terms\n        scopes\n\n        filters {{\n            budgets\n            has_free_delivery\n            has_online_payment\n            has_discount\n            is_voucher_enabled\n            tag_id\n            tags\n            cuisine {{\n                id\n                title\n            }}\n            food_characteristic {{\n                title\n                id\n            }}\n        }}\n        links {{\n            web_link\n        }}\n        voucher {{\n            voucher_code\n            is_voucher_saved\n        }}\n        external_integration\n    }}\n\n\n    fragment Carousels on Carousels {{\n        data {{\n            id\n            campaigns {{\n                ...CarouselItem\n            }}\n        }}\n    }}\n\n    \n    \n    fragment Swimlane on Swimlane {{\n        id\n        content_type\n        custom_strategy\n        filters {{\n            id\n            title\n            type\n            count\n        }}\n        headline\n        layout\n        traces\n        custom_meta {{\n            custom_layout\n        }}\n        vendors {{\n            vendor {{\n                ...Vendor\n            }}\n        }}\n    }}\n\n    fragment SwimlaneList on Swimlanes {{\n        data {{\n            items {{\n                ...Swimlane\n            }}\n        }}\n        meta {{\n            config_name\n            took\n            traces\n        }}\n        request_id\n        status\n    }}\n\n    \n    \n    fragment JokerVendor on Vendor {{\n        id\n        city {{\n            name\n        }}\n        code\n        name\n        delivery_fee_type\n        distance\n        minimum_delivery_time\n        minimum_pickup_time\n        rating\n        review_number\n        hero_listing_image\n        budget\n        minimum_delivery_fee\n        minimum_order_amount\n        primary_cuisine_id\n        cuisines {{\n            id\n            name\n            url_key\n        }}\n        url_key\n        is_active\n        food_characteristics {{\n            id\n            name\n        }}\n    }}\n\n    fragment JokerOffer on JokerOffers {{\n        offer_id\n        currency\n        status\n        status_text\n        items {{\n            reservation_code\n            is_last_promotion\n            rank\n            status\n            status_text\n            vendor {{\n                code\n                details {{\n                    ...JokerVendor\n                }}\n            }}\n        }}\n        remaining_duration\n        creation_date\n        expiration_date\n        tiers {{\n            discount {{\n                value\n                maximum_amount\n            }}\n            tier_id\n            mov\n        }}\n        current_tier_id\n        next_tier_id\n        amount_to_reach_next_tier\n        joker_fee\n        joker_voucher_code\n        joker_commission_base\n        tiers_type\n    }}\n\n    \n    \n    fragment DynamicSearchbarConfigData on DynamicSearchBarConfigData {{\n        type\n        message\n    }}\n\n\n    fragment DynamicSearchbarConfig on DynamicSearchBarConfig {{\n        data {{\n            ...DynamicSearchbarConfigData\n        }}\n    }}\n\n    \n    fragment ElementGroup on ElementGroup {{\n        id\n        elements {{\n            __typename\n            ... on Icon {{\n                icon_id\n                icon_decorators\n            }}\n            ... on Image {{\n                url\n            }}\n            ... on Separator {{\n                separator_id\n            }}\n            ... on Text {{\n                text_id\n                text\n                args\n                text_decorators\n            }}\n        }}\n    }}\n\n''',
                "variables": {{
                    "input": {{
                        "latitude": {lat},
                        "longitude": {lon},
                        "locale": "tr_TR",
                        "language_id": "2",
                        "customer_id": "",
                        "customer_type": "REGULAR",
                        "expedition_type": "DELIVERY",
                        "joker_offers": {{
                            "single_discount": False
                        }},
                        "feature_flags": [
                            {{
                                "name": "dynamic-pricing-indicator",
                                "value": "Original"
                            }}
                        ],
                        "subscription": {{
                            "status": "NON_ELIGIBLE",
                            "has_benefits": False
                        }},
                        "organic_listing": {{
                            "views": [
                                {{
                                    "budgets": "",
                                    "configuration": "Original",
                                    "cuisines": "",
                                    "discounts": "",
                                    "food_characteristics": "",
                                    "quick_filters": "",
                                    "use_free_delivery_label": True,
                                    "ncr_place": "list",
                                    "ncr_screen": "shop_list",
                                    "payment_types": "",
                                    "delivery_providers": "",
                                    "discount_labels": "",
                                    "tag_label_metadata": False,
                                    "limit": {limit},
                                    "offset": {offset}
                                }}
                            ]
                        }},
                        "swimlanes": {{
                            "config": "Original"
                        }}
                    }},
                    "includeCarousels": True,
                    "includeSwimlanes": True,
                    "includeJoker": False,
                    "includeDynamicSearchbarConfig": False
                }}
            }}
            """,
        )
        self.restaurant_stack = EntityValueStack()

    def _iterate_over_restaurants(self) -> Generator[dict, None, None]:
        offset = 0
        while 1:
            request_template = (
                self.filter_and_search_payload.retrieve_formatted_request(
                    {
                        "limit": 48,
                        "offset": offset,
                        "lat": self.geo_value.lat,
                        "lon": self.geo_value.lon,
                    }
                )
            )
            sync_call_params = SyncCallParams(**request_template)
            response = self.synchronized_call(sync_call_params)
            data = self._retrieve_json_from_response(response)

            if not data:
                break

            restaurants = (
                data.get("data", {})
                .get("rlp", {})
                .get("organic_listing", {})
                .get("views", [{}])[0]
                .get("items")
            )

            if not restaurants:
                break

            yield restaurants
            logger.info(
                f"page {offset} was crawled. total crawled data is {len(self.restaurant_stack)}"
            )

            offset += 1

    @staticmethod
    def transform_unstructured_data(record_value: dict) -> YemeksepetiRestaurantValue:
        pass

    def process(
        self, process_limit: int | None = None
    ) -> list[YemeksepetiRestaurantValue]:
        for restaurant_list in self._iterate_over_restaurants():
            for restaurant in restaurant_list:
                restaurant = self.transform_unstructured_data(restaurant)
                self.restaurant_stack.add_value(restaurant)

            if (
                process_limit is not None
                and len(self.restaurant_stack) >= process_limit
            ):
                break

        return self.restaurant_stack.retrieve_values()
