from datetime import datetime
from typing import Annotated
from uuid import UUID
import msgspec
from pydantic import BaseModel
from app.core.base_schema import BaseSchema, BaseStruct, CamelizedBaseStruct


class TenantBase(BaseSchema):
    name: str
    description: str | None = None


class AccountTenantAssociationCreate(BaseModel):
    account_id: UUID
    role: str


class AccountTenantAssociationUpdate(BaseModel):
    account_id: UUID | None = None
    role: str | None = None


class TenantCreate(BaseModel):
    name: str
    description: str | None = None

    accounts: list[AccountTenantAssociationCreate]


class TenantUpdate(TenantCreate):
    name: str | None = None
    description: str | None = None
    accounts: list[AccountTenantAssociationCreate] | None = None


class AccountRead(BaseSchema):
    username: str
    email: str


class AccountList(BaseModel):
    role: str
    account: AccountRead


class TenantRead(TenantBase):

    accounts: list[AccountList] = []
