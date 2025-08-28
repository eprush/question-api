"""
A module that implements endpoints of the type /questions
"""


from fastapi import APIRouter, status, HTTPException

from schemes.question import QuestionAddSchema
from src.core.dependencies  import (
    QuestionServiceDependence,
    AnswerServiceDependence,
)
from src.schemes.question import (
    QuestionSchema,
    AllQuestionsSchema,
    IDSchema,
    AnswersToQuestionSchema,
)
from src.schemes.problem import ProblemDetail


router = APIRouter(prefix="/questions", tags=["Работа с вопросами или их связями с ответами."])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": AllQuestionsSchema,
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
) -> AllQuestionsSchema:
    """ An endpoint for getting a list of all existing questions. """
    return question_service.get_all()


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
        data_to_add: QuestionAddSchema,
) -> QuestionSchema:
    """ An endpoint for adding a new question. """
    return question_service.create(data_to_add.text)


@router.get(
    "/{id_code}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": AnswersToQuestionSchema,
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
        id_code: IDSchema,
        question_service: QuestionServiceDependence,
        answer_service: AnswerServiceDependence,
) -> AnswersToQuestionSchema:
    """ An endpoint for getting a question by id and all the answers to it. """
    try:
        question = await question_service.get(id_code.id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Указан несуществующий номер вопроса.")
    answers = await answer_service.get_all(id_code.id)

    return AnswersToQuestionSchema(
        question=question,
        answers=answers
    )


@router.delete(
    "/{id_code}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": AnswersToQuestionSchema,
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
        id_code: IDSchema,
        question_service: QuestionServiceDependence,
        answer_service: AnswerServiceDependence,
) -> AnswersToQuestionSchema:
    """ An endpoint for getting a question by id and all the answers to it. """
    try:
        question = await question_service.delete(id_code.id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Указан несуществующий номер вопроса.")
    answers = await answer_service.get_all(id_code.id)

    return AnswersToQuestionSchema(
        question=question,
        answers=answers
    )

