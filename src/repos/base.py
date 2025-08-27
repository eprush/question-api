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
    def create(self, **kwargs) -> BaseModel:
        ...

    @abstractmethod
    def get_by_id(self, _id: int) -> BaseModel | None:
        ...

    @abstractmethod
    def get_all(self) -> tuple[BaseModel, ...]:
        ...

    @abstractmethod
    def delete_by_id(self, _id: int) -> None:
        ...