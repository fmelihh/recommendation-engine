from fastapi import FastAPI
from contextlib import asynccontextmanager

from .router import *

app = FastAPI()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("start up")
#     yield
#     print("tear down")


app.include_router(search_router, prefix="/search", tags=["Search"])
