import uvicorn
from fastapi import FastAPI

from src.recommendation_engine.app.environment import *
from src.recommendation_engine.app.shared_kernel.scheduler.celery_app import (
    celery_application,
)
from src.recommendation_engine.app.tasks import *


app = FastAPI()


@app.get("/")
def hello_world():
    return "hello world"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
