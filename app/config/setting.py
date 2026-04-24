from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_ENV_DIR = _PROJECT_ROOT / "env"




class Settings(BaseSettings):
    """
    Application Settings
    """

    model_config = SettingsConfigDict(
        env_file=f"{_ENV_DIR}/.env.{os.getenv('ENVIRONMENT', 'dev')}",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Environment Configuration
    environment: str = Field(default="dev", validation_alias="ENVIRONMENT")

    # Server Configuration
    server_host: str = Field(default="localhost", validation_alias="SERVER_HOST")
    server_port: int = Field(default=8001, validation_alias="SERVER_PORT")

    # Debug Configuration
    debug: bool = Field(default=True, validation_alias="DEBUG")
    
    # API Documentation Configuration
    title: str = Field(default="🎉 Liststar Admin 🎉 -Development", validation_alias="TITLE")
    version: str = Field(default="0.1.0", validation_alias="VERSION")
    summary: str = Field(default="API Summary", validation_alias="SUMMARY")
    root_path: str = Field(default="/api/v1", validation_alias="ROOT_PATH")
    description: str = Field(
        default="This is a web service framework based on python, based on Litestar and sqlalchemy implementation.",
        validation_alias="DESCRIPTION",
    )

    demo_enable: bool = Field(default=False, validation_alias="DEMO_ENABLE")

    # Database Configuration
    database_type: str = Field(default="mysql", validation_alias="DATABASE_TYPE")
    database_host: str = Field(default="localhost", validation_alias="DATABASE_HOST")
    database_port: int = Field(default=3308, validation_alias="DATABASE_PORT")
    database_username: str = Field(default="root", validation_alias="DATABASE_USERNAME")
    database_password: str = Field(default="root_password", validation_alias="DATABASE_PASSWORD")
    database_name: str = Field(default="litestaradmin", validation_alias="DATABASE_NAME")
    database_echo: bool = True

    # Log Setting
    logger_level: str = Field(default="DEBUG", validation_alias="LOGGER_LEVEL")

    @property
    def database_url(self) -> str:
        """
        Async SQLAlchemy database URL.

        Returns:
        - str: Connection string for the async driver.

        Raises:
        - ValueError: Raised when the database type is not supported.
        """
        if self.database_type not in ("mysql", "postgres", "sqlite"):
            raise ValueError(
                f"Unsupported database driver: {self.database_type}. For async databases, please choose mysql, postgres, or sqlite."
            )
        db_connect: str = ""
        if self.database_type == "mysql":
            db_connect = f"mysql+asyncmy://{self.database_username}:{quote_plus(self.database_password)}@{self.database_host}:{self.database_port}/{self.database_name}?charset=utf8mb4"
        elif self.database_type == "postgres":
            db_connect = f"postgresql+asyncpg://{self.database_username}:{quote_plus(self.database_password)}@{self.database_host}:{self.database_port}/{self.database_name}"
        else:
            db_connect = f"sqlite+aiosqlite:///{self.database_name}"
        return db_connect



@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
