from pydantic import BaseModel, Field
from app.core.base_schema import BaseSchema


class RoleBase(BaseSchema):
    name: str = Field(..., description="角色名稱")
    code: str = Field(..., description="角色代碼")
    description: str | None = Field(None, description="角色描述")


class RoleCreate(BaseModel):
    name: str = Field(..., description="角色名稱")
    code: str = Field(..., description="角色代碼")
    description: str | None = Field(None, description="角色描述")


class RoleUpdate(BaseModel):
    name: str | None = Field(None, description="角色名稱")
    code: str | None = Field(None, description="角色代碼")
    description: str | None = Field(None, description="角色描述")


class RoleRead(RoleBase):
    pass
