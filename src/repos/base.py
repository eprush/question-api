"""
A module describing base repository
"""
from abc import ABC, abstractmethod
from typing import Protocol, Generic, TypeVar

from src.models.base import BaseModel


class Model(Protocol):
    """ Model must have an id. """
    id: int


T = TypeVar("T", bound=Model)

class AbstractRepository(ABC, Generic[T]):
    model: BaseModel = T

    @abstractmethod
    async def create(self, **kwargs) -> BaseModel:
        ...

    @abstractmethod
    async def get_by_id(self, _id: int) -> BaseModel | None:
        ...

    @abstractmethod
    async def get_all(self, **kwargs) -> tuple[BaseModel, ...]:
        ...

    @abstractmethod
    async def delete_by_id(self, _id: int) -> BaseModel | None:
        ...