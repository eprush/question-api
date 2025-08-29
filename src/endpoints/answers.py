"""
A module that implements endpoints of the type /answers
"""


from fastapi import APIRouter, status, HTTPException


from src.core.dependencies import (
    AnswerServiceDependence,
)
from src.schemes.answer import (
    AnswerSchema,
)
from src.schemes.problem import ProblemDetail


router = APIRouter(prefix="/answers", tags=["Работа с ответами."])

@router.get(
    "/{id_code}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": AnswerSchema,
            "description": "Приложение доступно и работает.",
        },
        500: {
            "model": ProblemDetail,
            "description": "Внутренняя ошибка сервера.",
        },
    },
    description="Эндпоинт для получения ответа по id.",
)
async def read_answer(
        id_code: int,
        answer_service: AnswerServiceDependence,
) -> AnswerSchema:
    """ An endpoint for getting an answer by id. """
    try:
        return answer_service.get(id_code)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Указан несуществующий номер ответа.")


@router.delete(
    "/{id_code}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": AnswerSchema,
            "description": "Приложение доступно и работает.",
        },
        500: {
            "model": ProblemDetail,
            "description": "Внутренняя ошибка сервера.",
        },
    },
    description="Эндпоинт для удаления ответа по id.",
)
async def delete_answer(
        id_code: int,
        answer_service: AnswerServiceDependence,
) -> AnswerSchema:
    """ An endpoint for deleting an answer by id. """
    try:
        return answer_service.delete(id_code)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Указан несуществующий номер ответа.")
