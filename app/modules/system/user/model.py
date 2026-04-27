from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from app.core.base_model import Base


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, comment="Username"
    )
    email: Mapped[str | None] = mapped_column(
        String(64), nullable=True, unique=True, comment="Email address"
    )

    description: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="Description"
    )

    phone: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="Phone"
    )


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str = Field(..., description="必須填寫")
    email: str | None = Field(default=None, max_length=100, description="权限标识")
    description: str | None = Field(
        default=None, max_length=100, description="权限标识"
    )
    phone: str | None = Field(default=None, max_length=100, description="权限标识")
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., description="必須填寫")
    email: str | None = Field(default=None, max_length=100, description="权限标识")
    description: str | None = Field(
        default=None, max_length=100, description="权限标识"
    )
    phone: str | None = Field(default=None, max_length=100, description="权限标识")
    
class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    description: str | None = Field(
        default=None, max_length=100, description="权限标识"
    )
    phone: str | None = Field(default=None, max_length=100, description="权限标识")
