"""
A module that contains configuration src settings.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the application."""
    environment: str = "development"

    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_db: str = "database"
    postgres_username: str = "postgres"
    postgres_password: str = "example"
    pool_size: int = 2

    postgres_test_db: str = "test"

    @property
    def url_asyncpg(self) -> str:
        return (f"postgresql+asyncpg://{self.postgres_username}:{self.postgres_password}@"
                f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")

    @property
    def url_test_asyncpg(self) -> str:
        return (f"postgresql+asyncpg://{self.postgres_username}:{self.postgres_password}@"
                f"{self.postgres_host}:{self.postgres_port}/{self.postgres_test_db}")

    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE", ".env"))


@lru_cache
def get_app_settings() -> Settings:
    """Retrieve the application settings.

    Returns
    -------
        Settings: The application settings.

    """
    return Settings()

def get_settings_no_cache() -> Settings:
    """Получение настроек без кеша."""
    return Settings()