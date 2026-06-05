from pydantic import BaseModel, Field
from uuid import UUID
from app.core.base_schema import BaseSchema


class UserBase(BaseSchema):
    username: str = Field(..., description="賬戶名稱")
    email: str = Field(..., description="郵箱")
    created_by: UUID | None = Field(None, description="創建人")
    updated_by: UUID | None = Field(None, description="更新人")


class UserCreate(BaseModel):
    username: str = Field(..., description="賬戶名稱")
    email: str = Field(..., description="郵箱")
    password: str | None = Field(None, description="密碼")
    created_by: UUID | None = Field(None, description="創建人")


class UserUpdate(BaseModel):
    username: str | None = Field(None, description="賬戶名稱")
    email: str | None = Field(None, description="郵箱")
    password: str | None = Field(None, description="密碼")
    updated_by: UUID | None = Field(None, description="更新人")


class Role(BaseSchema):
    name: str = Field(..., description="角色名稱")
    code: str = Field(..., description="角色代碼")
    description: str | None = Field(None, description="角色描述")


class UserRead(UserBase):
    role_list: list[Role]
