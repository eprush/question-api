"""
The script that runs the application
"""

from fastapi import FastAPI, HTTPException
import uvicorn
import logging

from src.core.config import (
    Settings,
    get_app_settings,
)
from src.endpoints.api import routers
from src.core.logging import setup_json_logging
from src.core.handlers import (
    http_exception_handler,
    all_exception_handler,
)


def get_application() -> FastAPI:
    """Returns the FastAPI application instance."""
    settings: Settings = get_app_settings()

    if settings.environment != "development":
        setup_json_logging()
        logger = logging.getLogger("question-api")
        logger.warning("Running in production mode")


    application = FastAPI(
        **settings.model_dump(),
        title="Questions&Answers API",
        description="API-сервис для вопросов и ответов",
        separate_input_output_schemas=False,
        contact={
            "name": "eprush",
            "url": "https://github.com/eprush",
            "email": "pavlovich.er@phystech.edu"
        },
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/license/mit"
        },
    )

    application.include_router(routers)

    application.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
    application.add_exception_handler(Exception, all_exception_handler)
    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
