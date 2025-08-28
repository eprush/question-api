"""
A module describing repository, which can work with any data model
"""

from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic

from src.models.base import BaseModel
from src.repos.base import AbstractRepository, T


class Repository(AbstractRepository, Generic[T]):
    model: BaseModel | type = T

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def create(self, **values) -> BaseModel:
        """ A method for creating new record in the database. """
        statement = insert(self.model).values(**values).returning(self.model)
        result = await self._db_session.execute(statement)
        new_record = result.scalars().one()

        await self._db_session.commit()
        return new_record

    async def get_by_id(self, _id: int) -> BaseModel | None:
        """ Method for getting an animal by uuid. """
        statement = select(self.model).filter_by(id=_id)
        result = await self._db_session.execute(statement)
        return result.scalars().one_or_none()

    async def get_all(self, **where) -> tuple[BaseModel, ...]:
        """ Method for get all records in the database. """
        statement = select(self.model).filter_by(**where)
        result = await self._db_session.execute(statement)
        return tuple(result.scalars().all())

    async def delete_by_id(self, _id: int) -> BaseModel | None:
        statement = delete(self.model).filter_by(id=_id).returning(self.model)
        result = await self._db_session.execute(statement)
        deleted_record = result.scalars().one_or_none()

        await self._db_session.commit()
        return deleted_record
