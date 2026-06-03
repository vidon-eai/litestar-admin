import hashlib
from pydantic import BaseModel, Field, field_validator
from app.core.base_schema import BaseSchema


class AccountBase(BaseSchema):
    username: str = Field(..., description="賬戶名稱")
    email: str = Field(..., description="郵箱")


class AccountCreate(BaseModel):
    username: str = Field(..., description="賬戶名稱")
    email: str = Field(..., description="郵箱")
    hashed_password: str | None = Field(
        default=None, description="密碼", alias="password"
    )

    @field_validator("hashed_password", mode="before")
    @classmethod
    def hash_the_password(cls, v: str) -> str:
        clean_password = v.strip()
        return hashlib.sha256(clean_password.encode()).hexdigest()


class AccountUpdate(BaseModel):
    username: str | None = Field(None, description="賬戶名稱")
    email: str | None = Field(None, description="郵箱")
    hashed_password: str | None = Field(None, description="密碼", alias="password")


class AccountRead(AccountBase):
    pass
