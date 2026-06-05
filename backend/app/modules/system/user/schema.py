from pydantic import BaseModel, Field
from app.core.base_schema import BaseSchema


class UserBase(BaseSchema):
    username: str = Field(..., description="賬戶名稱")
    email: str = Field(..., description="郵箱")


class UserCreate(BaseModel):
    username: str = Field(..., description="賬戶名稱")
    email: str = Field(..., description="郵箱")
    password: str | None = Field(None, description="密碼")


class UserUpdate(BaseModel):
    username: str | None = Field(None, description="賬戶名稱")
    email: str | None = Field(None, description="郵箱")
    password: str | None = Field(None, description="密碼")


class Role(BaseSchema):
    name: str = Field(..., description="角色名稱")
    code: str = Field(..., description="角色代碼")
    description: str | None = Field(None, description="角色描述")


class UserRead(UserBase):
    role_list: list[Role]
