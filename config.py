import os

APP_NAME = "Esguvi - Security Auditor"

DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

ALLOWED_LOCAL_TARGETS = ["localhost", "127.0.0.1"]
