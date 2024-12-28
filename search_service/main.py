import uvicorn


from src.search.tasks.celery_app import celery_application

# noinspection PyUnresolvedReferences
from src.search.api import *

# noinspection PyUnresolvedReferences
from src.search import *

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
