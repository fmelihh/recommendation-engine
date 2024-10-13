import uvicorn
from fastapi import FastAPI

# noinspection PyUnresolvedReferences
from src.recommendation_engine.app.environment import *

# noinspection PyUnresolvedReferences
from src.recommendation_engine.app.shared_kernel.scheduler.celery_app import (
    celery_application,
)

# noinspection PyUnresolvedReferences
from src.recommendation_engine.app.tasks import *

# noinspection PyUnresolvedReferences
from src.recommendation_engine.app import *


app = FastAPI()


@app.get("/")
def hello_world():
    return "hello world"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
