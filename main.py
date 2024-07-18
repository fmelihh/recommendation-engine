import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from src.recommendation_engine.app.shared_kernel.scheduler.celery_app import (
    celery_application,
)
from src.recommendation_engine.app.tasks import *

env = os.getenv("ENVIRONMENT", "local")

if env == "docker":
    load_dotenv(".env.docker")
else:
    load_dotenv(".env.local")


app = FastAPI()


@app.get("/")
def hello_world():
    return "hello world"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
