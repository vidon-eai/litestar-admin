from datetime import datetime
from typing import Annotated, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
import msgspec


class BaseStruct(msgspec.Struct):
    def to_dict(self) -> dict[str, Any]:
        return {
            f: getattr(self, f)
            for f in self.__struct_fields__
            if getattr(self, f, None) != msgspec.UNSET
        }


class CamelizedBaseStruct(BaseStruct, rename="camel"):
    """Camelized Base Struct"""

    id: Annotated[UUID | None, msgspec.Meta(description="Primary Key")]
    created_at: Annotated[datetime, msgspec.Meta(description="Create record datetime")]
    updated_at: Annotated[datetime, msgspec.Meta(description="Update record datetime")]


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None, description="Primary Key")
    created_at: datetime = Field(..., description="Create record datetime")
    updated_at: datetime = Field(..., description="Update record datetime")


class TenantRead(CamelizedBaseStruct):
    name: str


class TenantCreate(BaseSchema):
    name: str


class AccountRead(CamelizedBaseStruct):
    username: str
    email: str | None


class TenantRole(CamelizedBaseStruct):
    account_id: UUID
    tenant_id: UUID
    role: str


class TenantWithAccounts(TenantRole):
    account: AccountRead


class AccountWithTenantRole(TenantRole):
    tenant: TenantRead


class AccountDetail(AccountRead):
    tenants: list[AccountWithTenantRole] = []


class TenantDetail(TenantRead):
    accounts: list[TenantWithAccounts] = []
