import uvicorn
from fastapi import FastAPI, UploadFile, File

from service import SearchService

app = FastAPI()


@app.get("/search-restaurant")
def search_restaurant(text: str, page: int = 0, total_page: int = 10):
    pass


@app.get("restaurant-upload")
async def restaurant_upload(file: UploadFile = File(...)):
    content = await file.read()
    SearchService().data_upload(content, file.content_type)

    return {"info": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
