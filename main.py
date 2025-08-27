"""
The script that runs the application
"""

from fastapi import FastAPI
import uvicorn

from src.core.config import (
    Settings,
    get_app_settings,
)
from src.endpoints.api import routers


def get_application() -> FastAPI:
    """Returns the FastAPI application instance."""
    settings: Settings = get_app_settings()


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
    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
