from __future__ import annotations
from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str = Field(..., description="必須填寫")
    content: str | None = Field(default=None, max_length=100, description="权限标识")
    user_id: UUID
    is_publish: bool = Field(default=False)
    created_at: datetime
    updated_at: datetime

class PostCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(..., description="必須填寫")
    content: str | None = Field(default=None, max_length=100, description="权限标识")
    user_id: UUID = Field(...)
    is_publish: bool = Field(default=False)
