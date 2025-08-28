from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid

from src.schemes.common import IDSchema


class AnswerAddSchema(BaseModel):
    text: str = Field(
        ...,
        max_length=1024,
        description="Текст ответа на интересующий вопрос. Максимальный размер 1024 символа.",
        examples=["Легко! Просто используйте встроенную функцию print."]
    )

    user_id: uuid.UUID = Field(
        ...,
        examples=[uuid.uuid4()],
        description="Уникальный нечисловой код соответствующий данному пользователю.",
    )

    model_config = ConfigDict(from_attributes=True)


class AnswerSchema(AnswerAddSchema, IDSchema):
    created_at: datetime = Field(
        ...,
        le=datetime.now(),
        examples=["2025-06-02 23:05:09.377698+03"],
        description="Дата и время добавления ответа на вопрос."
    )

    question_id: int = Field(
        ...,
        ge=0,
        description="Уникальный номер, соответствующий данному вопросу.",
        examples=[0, 10,]
    )

class AllAnswersSchema(BaseModel):
    answers: tuple[AnswerSchema, ...] = Field(
        ...,
        description="Список некоторых ответов.",
    )
