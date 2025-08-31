"""
A module describing repository, which can work with any data model
"""

from sqlalchemy import insert, select, delete
from typing import Sequence

from src.repos.base import BaseRepository, M


class AlchemyRepository(BaseRepository[M]):
    async def create(self, **values) -> M:
        """ A method for creating new record in the database. """
        statement = insert(self.Model).values(**values).returning(self.Model)
        result = await self._db_session.execute(statement)
        new_record = result.scalars().one()

        await self._db_session.commit()
        return new_record

    async def get_by_id(self, _id: int) -> M | None:
        """ Method for getting a record by id. """
        statement = select(self.Model).filter_by(id=_id)
        result = await self._db_session.execute(statement)
        return result.scalars().one_or_none()

    async def get_all(self, **where) -> tuple[M, ...]:
        """ Method for getting all records in the database. """
        statement = select(self.Model).filter_by(**where)
        result = await self._db_session.execute(statement)
        return tuple(result.scalars().all())

    async def delete_by_id(self, _id: int) -> M | None:
        """ Method for deleting a record by id. """
        statement = delete(self.Model).filter_by(id=_id).returning(self.Model)
        result = await self._db_session.execute(statement)
        deleted_record = result.scalars().one_or_none()

        await self._db_session.commit()
        return deleted_record
