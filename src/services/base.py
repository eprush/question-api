from typing import Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession

from src.repos.base import M, BaseRepository
from src.repos.common import AlchemyRepository


class BaseService(Generic[M]):
    """
    A service (сlass responsible for main logic) interface.
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
        self._repository: BaseRepository[M] = AlchemyRepository[M](model, db_session=db_session)

