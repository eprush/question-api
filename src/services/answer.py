import uuid

from src.services.base import BaseService
from src.models.answer import Answer
from src.schemes.answer import AnswerSchema


class AnswerService(BaseService[Answer]):
    async def create(self, text: str, *, question_id: int, user_id: uuid.UUID) -> AnswerSchema:
        new_obj = await self._repository.create(text=text, question_id=question_id, user_id=user_id)
        return AnswerSchema.model_validate(new_obj)

    async def get(self, _id: int) -> AnswerSchema:
        obj = await self._repository.get_by_id(_id)
        if obj is not None:
            return AnswerSchema.model_validate(obj)
        raise ValueError(f"A record number {_id} was not found.")

    async def delete(self, _id: int) -> AnswerSchema:
        obj = await self._repository.delete_by_id(_id)
        if obj is not None:
            return AnswerSchema.model_validate(obj)
        raise ValueError(f"A record number {_id} was not found.")
