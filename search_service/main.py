import uvicorn
from fastapi import FastAPI, UploadFile, File, Depends

from service import SearchService

app = FastAPI()

def convert_bytes_to_dataframe(content: bytes, content_type: str) -> pd.DataFrame:
    if content_type not in ("text/csv",):
        raise ValueError("unsupported file type")

    buffer = io.BytesIO(content)
    df = pd.read_csv(buffer)
    buffer.close()

    return df


@app.get("/search-restaurant")
def search_restaurant(
    text: str,
    page: int = 0,
    total_page: int = 10
):
    pass


@app.get("restaurant-upload")
async def restaurant_upload(file: UploadFile = File(...)):
    content = await file.read()
    df = convert_bytes_to_dataframe(content=content, content_type=file.content_type)
    search_service.upload_data(df=df)
    await file.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
