from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime

from src.schemes.common import IDSchema
from src.schemes.answer import AnswerSchema


class QuestionAddSchema(BaseModel):
    text: str = Field(
        ...,
        max_length=128,
        description="Текст интересующего вопроса. Максимальный размер 128 символов.",
        examples=["Как можно написать 'Hello, World!' на Python?"]
    )

    model_config = ConfigDict(from_attributes=True)


class QuestionSchema(QuestionAddSchema, IDSchema):
    created_at: datetime = Field(
        ...,
        le=datetime.now(),
        examples=["2025-06-02 23:05:09.377698+03"],
        description="Дата и время добавления вопроса."
    )


class AnswersToQuestionSchema(BaseModel):
    question: QuestionSchema
    answers: tuple[AnswerSchema, ...] = Field(
        ...,
        description="Список ответов на данный вопрос.",
    )

    @model_validator(mode="after")
    def is_answers_connect_with_question(self):
        for answer in self.answers:
            if answer.question_id != self.question.id:
                raise ValueError(f"The answer {answer.id} does not match the question {self.question.id}")
        return


class AllQuestionsSchema(BaseModel):
    questions: tuple[QuestionSchema, ...] = Field(
        ...,
        description="Список всех вопросов.",
    )