import os

ENVIRONMENT=os.getenv("ENVIRONMENT", "production")
BASE_PATH = os.getenv("APP_BASE_PATH", "")
URL_PREFIX = os.getenv("APP_URL_PREFIX", "")
BASE_URL = BASE_PATH + URL_PREFIX

REGISTRY_SERVICE_URL = os.getenv("REGISTRY_SERVICE_URL")

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL")

#APP_ID = os.getenv("LWARE_IDENTITY_USER", "")
APP_ID = os.getenv("APP_ID", "") if 'local' in ENVIRONMENT else os.getenv("LWARE_IDENTITY_USER", "")


UPLOAD_PATH = os.getenv("UPLOAD_PATH")
