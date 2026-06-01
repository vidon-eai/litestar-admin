from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None, description="Primary Key")
    created_at: datetime = Field(..., description="Create record datetime")
    updated_at: datetime = Field(..., description="Update record datetime")


class TenantRead(BaseSchema):
    name: str = Field(..., description="租戶名稱")


class TenantCreate(BaseModel):
    name: str = Field(..., description="租戶名稱")


class AccountRead(BaseSchema):

    username: str = Field(..., description="用戶名")
    email: str | None = Field(default=None, description="電郵")


class TenantRole(BaseModel):
    account_id: UUID = Field(..., description="帳號ID")
    tenant_id: UUID = Field(..., description="租戶ID")
    role: str = Field(..., description="在租戶中的角色")


class TenantWithAccounts(BaseSchema, TenantRole):
    account: AccountRead = Field(..., description="帳號")


class AccountWithTenantRole(BaseSchema, TenantRole):
    tenant: TenantRead = Field(..., description="租戶")


class AccountDetail(AccountRead):
    tenants: list[AccountWithTenantRole] = Field(
        default_factory=list, description="租戶列表"
    )


class TenantDetail(TenantRead):
    accounts: list[TenantWithAccounts] = Field(default_factory=list, description="帳號")
