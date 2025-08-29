"""
The module describing logging
"""

import logging
from pythonjsonlogger import json


def setup_json_logging() -> None:
    """Set up JSON logging."""
    logging.getLogger().handlers.clear()  # Cleaning up existing handlers

    formatter = json.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)

    # Disabling handler inheritance for "unicorn" loggers
    logging.getLogger("uvicorn").propagate = False
    logging.getLogger("uvicorn.access").propagate = False
    logging.getLogger("uvicorn.error").propagate = False

    # Installing a handler and formatter for loggers
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "FastAnimals"]:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()  # Clearing existing handlers, if any
        logger.setLevel(logging.INFO)
        logger.addHandler(log_handler)
