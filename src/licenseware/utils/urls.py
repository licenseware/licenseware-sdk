import os


BASE_URL = os.getenv("APP_BASE_PATH", "") + os.getenv("APP_URL_PREFIX", "") 