import pandas as pd
from typing import Any
import sqlalchemy as sa
from clickhouse_sqlalchemy import select

from ...menu.db import MenuModel
from ...comments.db import CommentsModel
from ...restaurants.db import RestaurantModel
from ....shared_kernel.database.clickhouse import get_session


class AggregateDomainsService:
    @staticmethod
    def retrieve_aggregate_data_detail(restaurant_id: str):
        query = AggregateDomainsService.generate_aggregate_data_query()
        query = query.where(
            sa.column("restaurant_id") == restaurant_id
        )

        with get_session() as session:
            column_names = [col.name for col in query.columns]
            compiled_cte = query.compile(compile_kwargs={"literal_binds": True})
            res = pd.DataFrame(
                columns=column_names,
                data=session.execute(sa.text(str(compiled_cte))).all(),
            )

            data = AggregateDomainsService.format_data(res)
            if len(data) > 0:
                return data[0]


    @staticmethod
    def retrieve_aggregate_data(
        page: int = 1, page_size: int = 10
    ) -> list[dict[str, Any]]:
        query = AggregateDomainsService.generate_aggregate_data_query()
        query = query.limit(page_size).offset((page - 1) * page_size)

        with get_session() as session:
            column_names = [col.name for col in query.columns]
            compiled_cte = query.compile(compile_kwargs={"literal_binds": True})
            res = pd.DataFrame(
                columns=column_names,
                data=session.execute(sa.text(str(compiled_cte))).all(),
            )

            data = AggregateDomainsService.format_data(res)
            return data


    @staticmethod
    def generate_aggregate_data_query() -> sa.Select:
        comments = (
            sa.select(
                sa.column("restaurant_id"),
                sa.func.groupArray(sa.column("comment")).label("comments"),
                sa.func.avg(sa.column("rating")).label("comment_avg_rating"),
            )
            .select_from(CommentsModel.__table__)
            .group_by(sa.column("restaurant_id"))
        ).cte("comments")

        menu = (
            sa.select(
                sa.column("restaurant_id"),
                sa.func.groupArray(sa.column("category")).label("product_categories"),
                sa.func.groupArray(sa.column("name")).label("product_names"),
                sa.func.groupArray(sa.column("description")).label(
                    "product_description"
                ),
            )
            .select_from(MenuModel.__table__)
            .group_by(sa.column("restaurant_id"))
        ).cte("menu")

        restaurants = (
            sa.select(
                sa.column("restaurant_id"),
                sa.column("provider"),
                sa.column("review_number"),
                sa.column("name").label("restaurant_name"),
                sa.column("rating").label("restaurant_rate"),
                sa.column("lat"),
                sa.column("lon"),
                sa.column("city").label("restaurant_city"),
            ).select_from(RestaurantModel.__table__)
        ).cte("restaurants")

        query = (
            select(restaurants.c, comments.c, menu.c)
            .select_from(restaurants)
            .join(
                comments,
                comments.c.restaurant_id == restaurants.c.restaurant_id,
                isouter=True,
            )
            .join(
                menu,
                menu.c.restaurant_id == restaurants.c.restaurant_id,
                isouter=True,
            )
        )
        return query


    @staticmethod
    def format_data(res: pd.DataFrame) -> list[dict[str, Any]]:
        res.columns = [col.split(".")[-1] for col in res.columns]
        for col in res.columns:
            if "%" in col:
                del res[col]

        data = res.to_dict(orient="records")
        for row in data:
            for row_key in row:
                if isinstance(row[row_key], list):
                    row[row_key] = list(set(row[row_key]))

        return data

