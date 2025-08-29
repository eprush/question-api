"""
A module describing handlers for different types of errors
"""

import logging
from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.schemes.problem import ProblemDetail


logger = logging.getLogger("question-api")


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:  # noqa: ARG001
    """Handle HTTP exceptions and return a JSON response.

    Args:
    ----
        request (Request): The request object.
        exc (HTTPException): The HTTP exception.

    Returns:
    -------
        JSONResponse: The JSON response.

    """
    logger.error(exc.detail)
    problem_detail = ProblemDetail(
        type="internal_server_error",
        status=exc.status_code,
        title="Внутренняя ошибка сервера",
        text=exc.detail or "Произошла ошибка при обработке запроса.",
        detail=[],
    )

    match exc.status_code:
        case status.HTTP_404_NOT_FOUND:
            problem_detail = ProblemDetail(
                type="not_found",
                title="Ресурс не найден",
                text=exc.detail or "Запрашиваемый ресурс не найден.",
                status=exc.status_code,
                detail=[],
            )
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            problem_detail = ProblemDetail(
                type="internal_server_error",
                title="Внутренняя ошибка сервера",
                text=exc.detail or "Произошла неожиданная ошибка.",
                status=exc.status_code,
                detail=[],
            )

    return JSONResponse(
        content=problem_detail.model_dump(exclude_none=True),
        status_code=exc.status_code,
    )


async def all_exception_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    """Handle all unhandled exceptions and return a JSON response.

    Args:
    ----
        request (Request): The request object.
        exc (Exception): The unhandled exception.

    Returns:
    -------
        JSONResponse: The JSON response.

    """
    logger.error(exc)
    problem_detail = ProblemDetail(
        type="internal_server_error",
        title="Внутренняя ошибка сервера",
        text="Произошла неожиданная ошибка.",
        status=500,
        detail=[],
    )
    return JSONResponse(
        content=problem_detail.model_dump(exclude_none=True),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )