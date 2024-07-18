import os
import dotenv

env = os.getenv("ENVIRONMENT", "local")
(
    dotenv.load_dotenv(".env.docker")
    if env == "docker"
    else dotenv.load_dotenv(".env.local")
)
