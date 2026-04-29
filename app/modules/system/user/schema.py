from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str = Field(..., description="必須填寫")
    email: str | None = Field(default=None, max_length=100, description="权限标识")
    description: str | None = Field(
        default=None, max_length=100, description="权限标识"
    )
    phone: str | None = Field(default=None, max_length=100, description="权限标识")
    address: str
    is_active: bool = True
    dob: datetime | None
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
