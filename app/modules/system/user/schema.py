from __future__ import annotations
from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.system.post.schema import PostRead

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
    
    posts: list[PostRead] | None = Field(default=[])
    
class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., description="必須填寫")
    email: str | None = Field(default=None, max_length=100, description="权限标识")
    description: str | None = Field(
        default=None, max_length=100, description="权限标识"
    )
    phone: str | None = Field(default=None, max_length=100, description="权限标识")
    is_active: bool = Field(default=False)
    dob: date | None = Field(default=None)
    address: str | None = Field(default=None)


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str | None = Field(default=None, max_length=100, description="权限标识")
    description: str | None = Field(
        default=None, max_length=100, description="权限标识"
    )
    phone: str | None = Field(default=None, max_length=100, description="权限标识")
    is_active: bool = Field(default=False)
    dob: date | None = Field(default=None)
    address: str | None = Field(default=None)
