"""ASGI entrypoint for production deployment."""
import os
os.environ.setdefault("APP_ENV", "production")

from lawim_v2.communication import app
