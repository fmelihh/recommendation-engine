from loguru import logger
from typing import Generator

from ..values import GeoValue
from .....shared_kernel.entity import BaseEntity
from .....shared_kernel.processor import Processor
from .....shared_kernel.request import RequestValue
from .....shared_kernel.processor import SyncCallParams
from .....shared_kernel.value_stack import EntityValueStack
from ..values.yemeksepeti import YemeksepetiRestaurantValue


class YemeksepetiRestaurants(BaseEntity, Processor):
    HEADERS = {
        'Referer': 'https://www.yemeksepeti.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
        'Host': 'tr.fd-api.com',
        'Origin': 'https://www.yemeksepeti.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Site': 'cross-site',
        'Content-Length': '12639',
        'Connection': 'keep-alive',
        'Authorization': 'Bearer Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOlsxXSwiZXhwIjozNTE2Mjg4MTA1LCJzdWIiOiJ0dG11dWRAZ21haWwuY29tIiwiY29tcGFueV9pZGVudGlmaWVyIjoidHRfbXV1ZF91c2VyIiwiaXNfc2VydmljZSI6ZmFsc2V9.Io-7tX4TOYGBrPHvt9Gu1-L5fpy_tSE_t0w9s2w36is',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'Request-Id': 'c27e3726-0c9d-44c9-8959-c2ddb7d8a084',
        'X-FP-API-KEY': 'volo',
        'perseus-session-id': '1731008747698.395883673882935828.p3lf6jtoyy',
        'perseus-client-id': '1731008747697.711480228086526878.alpf6f0b2w',
        'Platform': 'web',
        'dps-session-id': 'eyJzZXNzaW9uX2lkIjoiN2Y1MTkwY2VmOWMxYjM3YjU2NjQ4ZDdkMDU5MjRiNTQiLCJwZXJzZXVzX2lkIjoiMTczMTAwODc0NzY5Ny43MTE0ODAyMjgwODY1MjY4NzguYWxwZjZmMGIydyIsInRpbWVzdGFtcCI6MTczMTAwODc1M30=',
        'App-Version': 'VENDOR-LIST-MICROFRONTEND.24.45.0049'
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
        values = dict()
        values["name"] = record_value.get("name")
        values["rating"] = record_value.get("rating")
        values["url_slug"] = record_value.get("url_key")
        values["restaurant_id"] = record_value.get("id")
        values["review_number"] = record_value.get("review_number")
        values["coordinates"] = {
            "lat": record_value.get("latitude"),
            "lon": record_value.get("longitude"),
        }
        values["minimum_pickup_time"] = record_value.get("minimum_pickup_time")
        values["minimum_order_amount"] = record_value.get("minimum_order_amount")
        values["minimum_delivery_fee"] = record_value.get("minimum_delivery_fee")
        values["minimum_delivery_time"] = record_value.get("minimum_delivery_time")
        values["original_delivery_fee"] = record_value.get("original_delivery_fee")
        values["loyalty_percentage_amount"] = record_value.get(
            "loyalty_percentage_amount"
        )

        restaurant_value = YemeksepetiRestaurantValue(**values)
        return restaurant_value

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
