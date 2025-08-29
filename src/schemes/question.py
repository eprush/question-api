from pydantic import BaseModel, Field, ConfigDict, model_validator
import datetime

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
    created_at: datetime.datetime = Field(
        ...,
        examples=["2025-06-02 23:05:09.377698+03"],
        description="Дата и время добавления вопроса."
    )


class QuestionRelSchema(QuestionSchema):
    answers: list["AnswerSchema", ...] = Field(
        ...,
        description="Список ответов на данный вопрос.",
    )

    @model_validator(mode="after")
    def is_answers_connect_with_question(self):
        for answer in self.answers:
            if answer.question_id != self.id:
                raise ValueError(f"The answer {answer.id} does not match the question {self.id}")
        return self


class ListQuestionsSchema(BaseModel):
    questions: list[QuestionRelSchema, ...] = Field(
        ...,
        description="Список всех вопросов.",
    )