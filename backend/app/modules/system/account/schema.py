from dataclasses import dataclass
from typing import Sequence
from litestar.dto import DTOConfig, DataclassDTO
from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig
from pydantic import Field
from app.core.base_schema import BaseSchema
from app.db.models.models import Account


class AccountDTO(SQLAlchemyDTO[Account]):
    config = SQLAlchemyDTOConfig(exclude={"password"})


class AccountRead(BaseSchema):

    username: str = Field(..., description="用戶名")
    email: str | None = Field(default=None, description="電郵")
