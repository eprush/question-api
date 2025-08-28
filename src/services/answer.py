from sqlalchemy.ext.asyncio import AsyncSession

from src.models.answer import Answer
from src.repos.common import Repository
from src.repos.base import AbstractRepository
from src.schemes.answer import (
    AllAnswersSchema,
)


class AnswerService:
    def __init__(self, db_session: AsyncSession) -> None:
        self._repository: AbstractRepository[Answer] = Repository[Answer](db_session= db_session)

    async def get_all(self, _id: int) -> AllAnswersSchema:
        all_answers = await self._repository.get_all(question_id=_id)
        return AllAnswersSchema(answers=all_answers)

