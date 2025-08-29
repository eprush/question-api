from src.models.question import Question
from src.services.base import BaseService
from src.schemes.question import (
    QuestionSchema,
    QuestionRelSchema,
    ListQuestionsSchema,
)


class QuestionService(BaseService[Question]):
    async def create(self, text: str, **values) -> QuestionSchema:
        new_obj = await self._repository.create(text=text, **values)
        return QuestionSchema.model_validate(new_obj)

    async def get(self, _id: int) -> QuestionRelSchema:
        obj = await self._repository.get_by_id(_id)
        if obj is not None:
            return QuestionRelSchema.model_validate(obj)
        raise ValueError(f"A record number {_id} was not found.")

    async def delete(self, _id: int) -> QuestionRelSchema:
        obj = await self._repository.delete_by_id(_id)
        if obj is not None:
            return QuestionRelSchema.model_validate(obj)
        raise ValueError(f"A question number {_id} was not found.")

    async def get_all(self, **where) -> ListQuestionsSchema:
        all_objs = await self._repository.get_all(**where)
        return ListQuestionsSchema(questions=all_objs)
