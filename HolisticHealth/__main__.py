import logging
from typing import Dict

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from loguru import logger
from sentry_sdk.integrations.logging import (
    BreadcrumbHandler,
    EventHandler,
    LoggingIntegration,
)

import HolisticHealth
from HolisticHealth.config import settings
from HolisticHealth.logger import LOG_LEVEL

# Logging Config
environment = "production" if settings.production else "development"
sentry_sdk.init(
    settings.sentry_dsn,
    environment=environment,
    integrations=[LoggingIntegration(level=None, event_level=None)],
    traces_sample_rate=1.0,
)
logger.add(BreadcrumbHandler(level=logging.DEBUG), level=logging.DEBUG)
logger.add(EventHandler(level=logging.ERROR), level=logging.ERROR)

if environment == "production":
    logger.add(
        ".logs/{time}_access.log",
        rotation="50 MB",
        retention="15 days",
        filter="uvicorn",
        level=logging.DEBUG,
    )
    logger.add(
        ".logs/{time}_general.log",
        rotation="50 MB",
        retention="15 days",
        filter="HolisticHealth",
        level=logging.INFO,
    )
else:
    logger.add(
        ".logs/{time}_access.log",
        rotation="10 MB",
        retention="2 days",
        filter="uvicorn",
        level=logging.DEBUG,
    )
    logger.add(
        ".logs/{time}_general.log",
        rotation="10 MB",
        retention="2 days",
        filter="HolisticHealth",
        level=logging.INFO,
    )

# Create App Instance
logger.info(f"Starting Holistic Health API: {HolisticHealth.__version__}")
app = FastAPI()


@app.get("/")
def index() -> Dict[str, str]:
    return {"Production": str(settings.production)}


# Logging Config
UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "loggers": {
        "uvicorn": {"level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"level": "INFO", "propagate": settings.access_logs},
    },
}


if __name__ == "__main__":
    settings.validators.validate()
    uvicorn.run(
        "__main__:app",
        host="127.0.0.1",
        port=5000,
        log_level=LOG_LEVEL,
        log_config=UVICORN_LOGGING_CONFIG,
    )
