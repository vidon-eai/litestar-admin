import binascii
from functools import lru_cache
import os
from typing import Literal
from urllib.parse import quote_plus

from advanced_alchemy.config import AlembicAsyncConfig
from advanced_alchemy.extensions.litestar.plugins.init.config.engine import EngineConfig
from pydantic import Field, PositiveInt, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
)

from app.common.enums import StorageTypeEnum

from app.config.path_config import ALEMBIC_CONFIG_DIR, ALEMBIC_CONFIG_FILE, ENV_DIR


class DatabaseSetting(BaseSettings):
    DB_TYPE: Literal["postgresql", "mysql", "sqlite"] = Field(
        description="Database type to use.",
        default="mysql",
    )

    DB_HOST: str = Field(
        default=...,
        description="Hostname or IP address of the database server.",
    )

    DB_PORT: PositiveInt = Field(
        default=...,
        description="Port number for database connection.",
    )

    DB_USERNAME: str = Field(
        default=...,
        description="Username for database authentication.",
    )

    DB_PASSWORD: str = Field(
        default=...,
        description="Password for database authentication.",
    )

    DB_DATABASE: str = Field(
        default=...,
        description="Name of the database to connect to.",
    )

    SQLALCHEMY_ECHO: bool = Field(
        description="If True, SQLAlchemy will log all SQL statements.",
        default=True,
    )

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI_SCHEME(self) -> str:
        return "postgresql+asyncpg" if self.DB_TYPE == "postgresql" else "mysql+asyncmy"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """
        Async SQLAlchemy database URL.

        Returns:
        - str: Connection string for the async driver.

        """
        return (
            f"sqlite+aiosqlite:///{self.DB_DATABASE}"
            if self.DB_TYPE == "sqlite"
            else (
                f"{self.SQLALCHEMY_DATABASE_URI_SCHEME}://"
                f"{quote_plus(self.DB_USERNAME)}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
            )
        )

    @property
    def DB_CONFIG(self) -> SQLAlchemyAsyncConfig:

        return SQLAlchemyAsyncConfig(
            connection_string=self.SQLALCHEMY_DATABASE_URI,
            before_send_handler="autocommit",
            session_config=AsyncSessionConfig(expire_on_commit=False),
            engine_config=EngineConfig(echo=self.SQLALCHEMY_ECHO),
            alembic_config=AlembicAsyncConfig(
                script_location=f"{ALEMBIC_CONFIG_DIR}",
                script_config=f"{ALEMBIC_CONFIG_FILE}",
            ),
        )


class APIDocSetting(BaseSettings):

    API_DOCS_ENABLED: bool = Field(
        description="If True, API documentation will be enabled.",
        default=True,
    )

    TITLE: str = Field(default="🎉 Liststar Admin 🎉 -Development")
    VERSION: str = Field(default="0.1.0")
    SUMMARY: str = Field(default="API Summary")
    DESCRIPTION: str = Field(
        default="This is a web service framework based on python, based on Litestar and sqlalchemy implementation.",
    )

class StorageSetting(BaseSettings):
    STORAGE_TYPE: StorageTypeEnum = Field(default=StorageTypeEnum.LOCAL)
    STORAGE_LOCAL_PATH: str = Field(default="./storage")


class LoggingSetting(BaseSettings):
    LOG_LEVEL: str = Field(default="DEBUG")

    LOG_FORMAT: str = Field(
        description="Format string for log messages",
        default=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )


class AppSetting(DatabaseSetting, APIDocSetting, LoggingSetting, StorageSetting):
    model_config = SettingsConfigDict(
        env_file=f"{ENV_DIR}/.env.{os.getenv('ENVIRONMENT', 'dev')}",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Environment Configuration
    ENV: str = Field(default="dev")

    # Server Configuration
    SERVER_HOST: str = Field(default="localhost")
    SERVER_PORT: int = Field(default=8001)

    # Debug Configuration
    DEBUG: bool = Field(default=True)

    SECRET_KEY: str = Field(
        default_factory=lambda: binascii.hexlify(os.urandom(32)).decode(
            encoding="utf-8"
        ),
    )

    ROOT_PATH: str = Field(default="/api/v1")


@lru_cache
def get_app_setting() -> AppSetting:
    return AppSetting()


app_setting = get_app_setting()
