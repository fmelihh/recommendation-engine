from sqlalchemy.sql import literal
from clickhouse_sqlalchemy import select
from sqlalchemy import select, func, and_, null

from ...menu.db import MenuModel
from ...comments.db import CommentsModel
from ...restaurants.db import RestaurantModel
from ....shared_kernel.database.clickhouse import get_session


class RecommendationAggregateDomainsService:
    @staticmethod
    def retrieve_aggregate_data_detail(page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size

        r = RestaurantModel.__table__.alias("r")
        c = CommentsModel.__table__.alias("c")
        m = MenuModel.__table__.alias("m")

        comment_json = RecommendationAggregateDomainsService._build_comment_query(c)
        menu_json = RecommendationAggregateDomainsService._build_menu_query(m)

        stmt = (
            (
                select(
                    r.c.restaurant_id,
                    r.c.name,
                    r.c.provider,
                    r.c.rating,
                    r.c.delivery_fee,
                    r.c.delivery_time,
                    r.c.city,
                    r.c.version,
                    func.groupArrayDistinct(
                        func.if_(
                            and_(c.c.id != "", c.c.id != null()), comment_json, null()
                        )
                    ).label("restaurant_comments"),
                    func.groupArrayDistinct(
                        func.if_(
                            and_(m.c.id != "", m.c.id != null()), menu_json, null()
                        )
                    ).label("menu_items"),
                )
                .select_from(
                    r.outerjoin(c, r.c.restaurant_id == c.c.restaurant_id).outerjoin(
                        m, r.c.restaurant_id == m.c.restaurant_id
                    )
                )
                .group_by(
                    r.c.restaurant_id,
                    r.c.name,
                    r.c.provider,
                    r.c.rating,
                    r.c.delivery_fee,
                    r.c.delivery_time,
                    r.c.city,
                    r.c.version,
                )
            )
            .limit(page_size)
            .offset(offset)
        )

        with get_session() as session:
            result = session.execute(stmt).fetchall()
        return result

    @staticmethod
    def _build_comment_query(comment_alias):
        return func.concat(
            literal("{"),
            '"id":"',
            comment_alias.c.id,
            '",',
            '"restaurant_id":"',
            comment_alias.c.restaurant_id,
            '",',
            '"provider":"',
            comment_alias.c.provider,
            '",',
            '"rating":',
            func.toString(comment_alias.c.rating),
            ",",
            '"comment":"',
            func.replaceRegexpAll(
                func.replaceOne(comment_alias.c.comment, '"', '\\"'), "\n|\r", " "
            ),
            '",',
            '"comment_id":"',
            comment_alias.c.comment_id,
            '",',
            '"replies":',
            func.if_(
                comment_alias.c.replies != null(),
                func.toJSONString(comment_alias.c.replies),
                "[]",
            ),
            ",",
            '"like_count":',
            func.toString(comment_alias.c.like_count),
            ",",
            '"created_at":"',
            func.if_(
                comment_alias.c.created_at != null(),
                func.toString(comment_alias.c.created_at),
                "",
            ),
            '",',
            '"updated_at":"',
            func.if_(
                comment_alias.c.updated_at != null(),
                func.toString(comment_alias.c.updated_at),
                "",
            ),
            '",',
            '"version":',
            func.toString(comment_alias.c.version),
            "}",
        )

    @staticmethod
    def _build_menu_query(menu_alias):
        return func.concat(
            literal("{"),
            '"id":"',
            menu_alias.c.id,
            '",',
            '"restaurant_id":"',
            menu_alias.c.restaurant_id,
            '",',
            '"provider":"',
            menu_alias.c.provider,
            '",',
            '"category":',
            func.if_(
                menu_alias.c.category != null(),
                func.concat('"', menu_alias.c.category, '"'),
                "null",
            ),
            ",",
            '"product_id":',
            func.if_(
                menu_alias.c.product_id != null(),
                func.concat('"', menu_alias.c.product_id, '"'),
                "null",
            ),
            ",",
            '"name":"',
            func.replaceOne(menu_alias.c.name, '"', '\\"'),
            '",',
            '"description":',
            func.if_(
                menu_alias.c.description != null(),
                func.concat(
                    '"', func.replaceOne(menu_alias.c.description, '"', '\\"'), '"'
                ),
                "null",
            ),
            ",",
            '"image_url":',
            func.if_(
                menu_alias.c.image_url != null(),
                func.concat('"', menu_alias.c.image_url, '"'),
                "null",
            ),
            ",",
            '"price":',
            func.toString(menu_alias.c.price),
            ",",
            '"price_currency":"',
            menu_alias.c.price_currency,
            '",',
            '"version":',
            func.toString(menu_alias.c.version),
            "}",
        )
