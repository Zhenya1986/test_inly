from os import getenv
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger('test_inly')

# ======= APP ==========
APP_HOST = getenv("APP_HOST", default="127.0.0.1")
APP_PORT = int(getenv("APP_PORT", default=8000))

# ======= BD ==========
BD_HOST = getenv("BD_HOST", default="")
BD_PORT = int(getenv("BD_PORT", default=5432))
BD_USER = getenv("BD_USER", default="postgres")
BD_PASSWORD = getenv("BD_PASSWORD", default="postgres")
BD_NAME = getenv("BD_NAME", default="mydatabase")


# ======= AUTH
COOKIES_KEY = getenv("COOKIES_KEY", default="user_cookie")
