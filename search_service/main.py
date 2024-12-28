import uvicorn

# noinspection PyUnresolvedReferences
from src.search.api import *


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
