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
        env_file=f"{_ENV_DIR}/.env.{os.getenv('ENVIRONMENT')}",
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
    database_user: str = Field(default="root", validation_alias="DATABASE_USER")
    database_password: str = Field(default="root_password", validation_alias="DATABASE_PASSWORD")
    database_name: str = Field(default="litestaradmin", validation_alias="DATABASE_NAME")

    # Log Setting
    logger_level: str = Field(default="DEBUG", validation_alias="LOGGER_LEVEL")


    # @field_validator("redis_user", "redis_password", mode="before")
    # @classmethod
    # def _empty_str_to_none(cls, v: Any) -> Any:
    #     if v == "":
    #         return None
    #     return v

    @property
    def database_url(self) -> str:
        """SQLAlchemy 同步連線字串（mysql+pymysql）。密碼會進行 URL 編碼。"""
        user = quote_plus(self.database_user)
        password = quote_plus(self.database_password)
        return (
            f"{self.database_type}+pymysql://{user}:{password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
