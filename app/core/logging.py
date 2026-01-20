"""Professional logging configuration with structured logging"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from pythonjsonlogger import jsonlogger

from app.core.config import settings

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields"""

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)

        # Add timestamp
        if not log_record.get("timestamp"):
            log_record["timestamp"] = datetime.utcnow().isoformat()

        # Add log level
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        # Add application info
        log_record["app_name"] = settings.APP_NAME
        log_record["app_version"] = settings.APP_VERSION
        log_record["environment"] = settings.ENVIRONMENT


def setup_logging() -> logging.Logger:
    """
    Setup structured logging with JSON format

    Features:
    - JSON formatted logs
    - Console and file handlers
    - Log rotation
    - Request correlation IDs
    - Structured error tracking
    """

    # Create logger
    logger = logging.getLogger("fastapi_app")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Prevent duplicate logs
    logger.handlers.clear()

    # JSON formatter
    json_formatter = CustomJsonFormatter(
        "%(timestamp)s %(level)s %(name)s %(message)s",
        rename_fields={
            "levelname": "level",
            "name": "logger_name",
            "threadName": "thread",
            "processName": "process",
        },
    )

    # Console handler (for development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    if settings.ENVIRONMENT == "development":
        # Human-readable format for development
        dev_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(dev_formatter)
    else:
        # JSON format for production
        console_handler.setFormatter(json_formatter)

    logger.addHandler(console_handler)

    # File handler (JSON format)
    if settings.ENVIRONMENT != "test":
        from logging.handlers import RotatingFileHandler

        # General application logs
        app_handler = RotatingFileHandler(
            LOGS_DIR / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(json_formatter)
        logger.addHandler(app_handler)

        # Error logs (separate file)
        error_handler = RotatingFileHandler(
            LOGS_DIR / "error.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(json_formatter)
        logger.addHandler(error_handler)

        # Access logs (HTTP requests)
        access_handler = RotatingFileHandler(
            LOGS_DIR / "access.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
        access_handler.setLevel(logging.INFO)
        access_handler.setFormatter(json_formatter)

        # Create separate logger for access logs
        access_logger = logging.getLogger("access")
        access_logger.setLevel(logging.INFO)
        access_logger.handlers.clear()
        access_logger.addHandler(access_handler)
        access_logger.propagate = False

    return logger


def get_logger(name: str = "fastapi_app") -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)


# Initialize logger
logger = setup_logging()
access_logger = logging.getLogger("access")
