"""
The module that defines the dependencies.
Among them, connection to the database, dependence on their own services
"""
from collections.abc import AsyncGenerator
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends

from src.core.config import Settings, get_app_settings
from src.services.question import QuestionService
from src.services.answer import AnswerService


app_settings: Settings = get_app_settings()

async_engine = create_async_engine(
    app_settings.url_asyncpg,
    pool_pre_ping=True,
    pool_size=app_settings.pool_size,
)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting a session with a database."""
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


DatabaseDependence = Annotated[AsyncSession, Depends(get_db)]


async def get_question_service(db: DatabaseDependence) -> QuestionService:
    """Returns an instance of QuestionService."""
    return QuestionService(db_session=db)


async def get_answer_service(db: DatabaseDependence) -> AnswerService:
    """Returns an instance of AnswerService."""
    return AnswerService(db_session=db)


QuestionServiceDependence = Annotated[QuestionService, Depends(get_question_service)]
AnswerServiceDependence = Annotated[AnswerService, Depends(get_answer_service)]
