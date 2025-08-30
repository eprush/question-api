"""
A module describing base repository
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import BaseModel


M = TypeVar("M", bound=BaseModel)


class BaseRepository(ABC, Generic[M]):
    def __init__(self, model: Type[M], *, db_session: AsyncSession) -> None:
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
        ...

    @abstractmethod
    async def delete_by_id(self, _id: int) -> M | None:
        ...