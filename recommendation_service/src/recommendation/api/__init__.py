from fastapi import FastAPI

from .routers import *
from ..services.model import retrieve_recommendation_model


app = FastAPI()
retrieve_recommendation_model()

app.include_router(recommendation_router, tags=["recommendation"])
