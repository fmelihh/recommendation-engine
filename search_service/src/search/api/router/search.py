from fastapi import APIRouter


search_router = APIRouter()


@search_router.get("/search")
def search():
    pass
