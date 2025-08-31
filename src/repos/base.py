"""
A module describing base repository
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import BaseModel

M = TypeVar("M", bound=BaseModel)


class BaseRepository(ABC, Generic[M]):
    """
    A repository (сlass responsible for interacting with the database) interface.
    Implements a common constructor.

    TypeVar:
    ----
        M (TypeVar("M", bound=BaseModel)): type of any SQLAlchemy data model.
    """

    def __init__(self, model: Type[M], *, db_session: AsyncSession) -> None:
        """
        Args:
        ----
            model (Type[M]): any SQLAlchemy data model.
            db_session (AsyncSession):  session for connect to database.
        """
        self._db_session = db_session
        self.Model: Type[M] = model

    @abstractmethod
    async def create(self, **values) -> M:
        ...

    @abstractmethod
    async def get_by_id(self, _id: int) -> M | None:
        ...

    @abstractmethod
    async def get_all(self, **where) -> tuple[M, ...]:
        """ A method for getting all records matching the where condition. """
        ...

    @abstractmethod
    async def delete_by_id(self, _id: int) -> M | None:
        ...
