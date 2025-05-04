from fastapi import FastAPI
from contextlib import asynccontextmanager

from .router import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start up")
    yield
    print("tear down")


app = FastAPI(lifespan=lifespan)

app.include_router(
    aggregate_domain_router, prefix="/aggregate_domain", tags=["Aggregate Domain"]
)
app.include_router(
    recommendation_aggregate_domain_router,
    prefix="/recommendation_aggregate",
    tags=["Recommendation Aggregate Domain"],
)
