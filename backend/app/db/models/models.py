from uuid import UUID
from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Account(UUIDv7AuditBase):
    __tablename__ = "accounts"

    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, comment="帳號名稱"
    )

    email: Mapped[str | None] = mapped_column(
        String(255), nullable=True, unique=True, comment="電子郵箱"
    )

    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密碼")

    tenants: Mapped[list["AccountTenantAssociation"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=True,
    )


class Tenant(UUIDv7AuditBase):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, comment="租戶名稱"
    )

    accounts: Mapped[list["AccountTenantAssociation"]] = relationship(
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=True,
    )


class AccountTenantAssociation(UUIDv7AuditBase):
    __tablename__ = "account_tenant_association"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, comment="帳號 ID"
    )

    tenant_id: Mapped[UUID] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, comment="租戶 ID"
    )

    role: Mapped[str] = mapped_column(String(255), nullable=False, comment="角色")

    account: Mapped["Account"] = relationship(
        back_populates="tenants",
        lazy="selectin",
    )

    tenant: Mapped["Tenant"] = relationship(
        back_populates="accounts",
        lazy="selectin",
    )
