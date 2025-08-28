from sqlalchemy.ext.asyncio import AsyncSession

from src.models.question import Question
from src.repos.common import Repository
from src.repos.base import AbstractRepository
from src.schemes.question import (
    QuestionSchema,
    AllQuestionsSchema,
)

class QuestionService:
    def __init__(self, db_session: AsyncSession) -> None:
        self._repository: AbstractRepository[Question] = Repository[Question](db_session= db_session)

    async def get_all(self) -> AllQuestionsSchema:
        all_questions = await self._repository.get_all()
        return AllQuestionsSchema(questions=all_questions)

    async def create(self, text: str) -> QuestionSchema:
        new_question = await self._repository.create(text=text)
        return QuestionSchema.model_validate(new_question)

    async def get(self, _id: int) -> QuestionSchema:
        question = await self._repository.get_by_id(_id)
        if question is not None:
            return QuestionSchema.model_validate(question)
        raise ValueError(f"A question number {_id} was not found.")

    async def delete(self, _id: int) -> QuestionSchema:
        question = await self._repository.delete_by_id(_id)
        if question is not None:
            return QuestionSchema.model_validate(question)
        raise ValueError(f"A question number {_id} was not found.")
