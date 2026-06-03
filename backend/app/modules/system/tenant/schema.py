from uuid import UUID
from pydantic import BaseModel, Field
from app.core.base_schema import BaseSchema


class TenantBase(BaseSchema):
    name: str = Field(..., description="租戶名稱")
    description: str | None = Field(None, description="租戶描述")


class TenantCreate(BaseModel):
    name: str = Field(..., description="租戶名稱")
    description: str | None = Field(None, description="租戶描述")


class TenantUpdate(TenantCreate):
    name: str | None = Field(None, description="租戶名稱")


class TenantRead(TenantBase):
    pass
