import uvicorn

from src.recommendation.api import *


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
