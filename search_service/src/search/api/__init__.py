from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(search_router, prefix="/search", tags=["Search"])
