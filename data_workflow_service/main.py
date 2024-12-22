import os
import dotenv
import uvicorn
import inspect
from loguru import logger
from sqlalchemy import inspect as sqlalchemy_inspect


env = os.getenv("ENVIRONMENT", "local")
(
    dotenv.load_dotenv(".env.docker")
    if env == "docker"
    else dotenv.load_dotenv(".env.local")
)


# noinspection PyUnresolvedReferences
from src.recommendation_engine.app.shared_kernel.scheduler.celery_app import (
    celery_application,
)

# noinspection PyUnresolvedReferences
from src.recommendation_engine.app.tasks import *

# noinspection PyUnresolvedReferences
from src.recommendation_engine.app.shared_kernel.database.clickhouse import (
    ClickhouseBase,
    engine,
)

# noinspection PyUnresolvedReferences
from src.recommendation_engine.app import *

# noinspection PyUnresolvedReferences
from src.recommendation_engine.app.shared_kernel.api import *


def create_tables():
    inspector = sqlalchemy_inspect(engine)

    for name, obj in globals().items():
        if inspect.isclass(obj):
            if issubclass(obj, ClickhouseBase) and obj != ClickhouseBase:
                if not inspector.has_table(obj.__tablename__):
                    obj.__table__.create(engine)
                    logger.info(f"{name} Clickhouse Table Created.")
                else:
                    logger.info(f"{name} Clickhouse Table Already Exists.")


if __name__ == "__main__":
    create_tables()
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
