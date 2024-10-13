import os
import inspect
import uvicorn
import dotenv
from loguru import logger
from fastapi import FastAPI



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
from src.recommendation_engine.app.shared_kernel.database.clickhouse import ClickhouseBase, engine

# noinspection PyUnresolvedReferences
from src.recommendation_engine.app import *


app = FastAPI()

def create_tables():
    for name, obj in globals().items():
        if inspect.isclass(obj):
            if issubclass(obj, ClickhouseBase) and obj != ClickhouseBase:
                obj.__table__.create(engine)
                logger.info(f"{name} Clickhouse Table Created.")



@app.get("/")
def hello_world():
    return "hello world"


if __name__ == "__main__":
    create_tables()
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
