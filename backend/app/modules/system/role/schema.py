from uuid import UUID

from app.core.base_schema import BaseSchema
from pydantic import BaseModel, Field


class RoleBase(BaseSchema):
    name: str = Field(..., description="角色名稱")
    code: str = Field(..., description="角色代碼")
    description: str | None = Field(None, description="角色描述")


class RoleCreate(BaseModel):
    name: str = Field(..., description="角色名稱")
    code: str = Field(..., description="角色代碼")
    description: str | None = Field(None, description="角色描述")
    created_by: UUID | None = Field(default=None)
    updated_by: UUID | None = Field(default=None)


class RoleUpdate(BaseModel):
    name: str | None = Field(None, description="角色名稱")
    code: str | None = Field(None, description="角色代碼")
    description: str | None = Field(None, description="角色描述")


class RoleRead(RoleBase):
    pass
