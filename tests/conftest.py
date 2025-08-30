import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
import pytest

from src.core.config import Settings, get_settings_no_cache
from src.core.dependencies import get_db
from src.models.base import BaseModel
from src.models.answer import Answer # noqa
from src.models.question import Question # noqa
from main import app


app_settings: Settings = get_settings_no_cache()


@pytest_asyncio.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
def engine():
    engine = create_async_engine(app_settings.url_test_asyncpg, pool_size=app_settings.pool_size)
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def prepare_db():
    create_db_engine = create_async_engine(
        app_settings.url_asyncpg,
        isolation_level="AUTOCOMMIT",
    )
    async with create_db_engine.begin() as connection:
        await connection.execute(
            text("drop database if exists {name};".format(name=app_settings.postgres_test_db)),
        )

        await connection.execute(
            text("create database {name};".format(name=app_settings.postgres_test_db)),
        )


@pytest_asyncio.fixture(scope="session")
async def db_session(engine) -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.drop_all)
        await connection.run_sync(BaseModel.metadata.create_all)
        TestingSessionLocal = sessionmaker(
            expire_on_commit=False,
            class_=AsyncSession,
            bind=engine,
        )
        async with TestingSessionLocal(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture(scope="session")
def override_get_db(prepare_db, db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest_asyncio.fixture(scope="session")
async def async_client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
