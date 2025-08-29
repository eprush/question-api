from typing import Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession

from src.repos.base import M, BaseRepository
from src.repos.common import AlchemyRepository


class BaseService(Generic[M]):
    def __init__(self, model: Type[M], *, db_session: AsyncSession) -> None:
        self._repository: BaseRepository[M] = AlchemyRepository[M](model, db_session=db_session)

