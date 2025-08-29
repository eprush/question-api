"""
A module that implements endpoints of the type /questions
"""


from fastapi import APIRouter, status, HTTPException

from src.core.dependencies  import (
    QuestionServiceDependence,
    AnswerServiceDependence,
)
from src.schemes.question import (
    QuestionAddSchema,
    QuestionSchema,
    QuestionRelSchema,
    ListQuestionsSchema,
)
from src.schemes.answer import (
    AnswerAddSchema,
    AnswerSchema,
)
from src.schemes.problem import ProblemDetail


router = APIRouter(prefix="/questions", tags=["Работа с вопросами или их связями с ответами."])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": ListQuestionsSchema,
            "description": "Приложение доступно и работает.",
        },
        500: {
            "model": ProblemDetail,
            "description": "Внутренняя ошибка сервера.",
        },
    },
    description="Эндпоинт для получения списка всех существующих (неудаленных) вопросов без ответов к ним.",
)
async def read_all_questions(
        question_service: QuestionServiceDependence,
) -> ListQuestionsSchema:
    """ An endpoint for getting a list of all existing questions. """
    tmp = await question_service.get_all()
    print(tmp)
    return tmp


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": QuestionSchema,
            "description": "Приложение доступно и работает.",
        },
        500: {
            "model": ProblemDetail,
            "description": "Внутренняя ошибка сервера.",
        },
    },
    description="Эндпоинт для добавления нового вопроса, то есть пока без ответа.",
)
async def add_new_question(
        question_service: QuestionServiceDependence,
        question_to_add: QuestionAddSchema,
) -> QuestionSchema:
    """ An endpoint for adding a new question. """
    return await question_service.create(question_to_add.text)


@router.get(
    "/{id_code}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": QuestionRelSchema,
            "description": "Приложение доступно и работает.",
        },
        404: {
            "model": ProblemDetail,
            "description": "Несуществующий вопрос.",
        },
        500: {
            "model": ProblemDetail,
            "description": "Внутренняя ошибка сервера.",
        },
    },
    description="Эндпоинт для получения вопроса по id и всех ответов к нему.",
)
async def read_question_with_its_answer(
        id_code: int,
        question_service: QuestionServiceDependence,
) -> QuestionRelSchema:
    """ An endpoint for getting a question by id and all the answers to it. """
    try:
        return await question_service.get(id_code)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Указан несуществующий номер вопроса.")


@router.delete(
    "/{id_code}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": QuestionRelSchema,
            "description": "Приложение доступно и работает.",
        },
        404: {
            "model": ProblemDetail,
            "description": "Несуществующий вопрос.",
        },
        500: {
            "model": ProblemDetail,
            "description": "Внутренняя ошибка сервера.",
        },
    },
    description="Эндпоинт для удаления вопроса по id и всех ответов к нему.",
)
async def delete_question_with_its_answer(
        id_code: int,
        question_service: QuestionServiceDependence,
) -> QuestionRelSchema:
    """ An endpoint for deleting a question by id and all the answers to it. """
    try:
        return await question_service.delete(id_code)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Указан несуществующий номер вопроса.")


@router.post(
    "/{id_code}/answers",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": AnswerSchema,
            "description": "Приложение доступно и работает.",
        },
        404: {
            "model": ProblemDetail,
            "description": "Несуществующий вопрос.",
        },
        500: {
            "model": ProblemDetail,
            "description": "Внутренняя ошибка сервера.",
        },
    },
    description="Эндпоинт для добавления ответа к вопросу по id.",
)
async def add_new_answer(
        id_code: int,
        answer_to_add: AnswerAddSchema,
        question_service: QuestionServiceDependence,
        answer_service: AnswerServiceDependence,
) -> AnswerSchema:
    """ An endpoint for adding an answer to a question by id. """
    try:
        await question_service.get(id_code)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Указан несуществующий номер вопроса.")
    answer = await answer_service.create(answer_to_add.text,
        question_id=id_code,
        user_id=answer_to_add.user_id
    )
    return answer
