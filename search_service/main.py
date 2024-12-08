import uvicorn
from fastapi import FastAPI

from service import SearchService

app = FastAPI()


@app.get("/search-restaurant")
def search_restaurant(text: str, page: int = 0, total_page: int = 10):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
