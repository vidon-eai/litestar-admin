from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from advanced_alchemy.types import PasswordHash
from advanced_alchemy.types.password_hash.argon2 import Argon2Hasher
from app.common.enums import StorageTypeEnum
from sqlalchemy import (
    JSON,
    BigInteger,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import UserMixin


class UserRole(UUIDv7AuditBase):
    __tablename__ = "sys_user_role"

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("sys_user.id", ondelete="CASCADE"), nullable=False
    )
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("sys_role.id", ondelete="CASCADE"), nullable=False
    )

    # 關聯數據
    user: Mapped["User"] = relationship(
        back_populates="roles", innerjoin=True, uselist=False, lazy="joined"
    )
    role: Mapped["Role"] = relationship(
        back_populates="users", innerjoin=True, uselist=False, lazy="joined"
    )


class User(UUIDv7AuditBase, UserMixin):
    __tablename__ = "sys_user"

    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, comment="用戶名/登錄帳號"
    )
    password: Mapped[str] = mapped_column(
        PasswordHash(backend=Argon2Hasher()),
        nullable=True,
        comment="密碼",
        default=None,
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, comment="電子郵箱"
    )
    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None, comment="描述"
    )

    is_active: Mapped[bool] = mapped_column(
        default=True, nullable=False, comment="是否啟用"
    )

    # 關聯數據
    roles: Mapped[list[UserRole]] = relationship(
        back_populates="user",
        lazy="selectin",
        uselist=True,
        cascade="all, delete-orphan",
    )
    creator: Mapped["User | None"] = relationship(
        "User",
        remote_side="User.id",
        foreign_keys="User.created_by",
        lazy="selectin",
        uselist=False,
        viewonly=True,
    )
    updater: Mapped["User | None"] = relationship(
        "User",
        remote_side="User.id",
        foreign_keys="User.updated_by",
        lazy="selectin",
        uselist=False,
        viewonly=True,
    )
    role_list: AssociationProxy[list["Role"]] = association_proxy(
        "roles", "role", creator=lambda role: UserRole(role=role)
    )
    role_ids: AssociationProxy[list[UUID]] = association_proxy(
        "roles", "role_id", creator=lambda rid: UserRole(role_id=rid)
    )


class Role(UUIDv7AuditBase, UserMixin):
    __tablename__ = "sys_role"

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="角色名稱")
    code: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, comment="角色代碼"
    )
    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None, comment="描述"
    )

    # 關聯數據
    users: Mapped[list[UserRole]] = relationship(
        back_populates="role",
        cascade="all, delete",
        lazy="noload",
        viewonly=True,
    )


class AuditLog(UUIDv7AuditBase):
    __tablename__ = "sys_audit_log"

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sys_user.id", ondelete="SET NULL"),
        nullable=True,
        comment="操作者 ID",
    )
    request_method: Mapped[str] = mapped_column(
        String(50), comment="GET, POST, PUT, DELETE"
    )
    request_path: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="API 路徑"
    )
    request_payload: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="請求內容"
    )
    request_ip: Mapped[str | None] = mapped_column(
        String(45), nullable=True, comment="操作者 IP"
    )
    status_code: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="HTTP 狀態碼"
    )
    response_body: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="回應內容"
    )


class File(UUIDv7AuditBase):
    __tablename__ = "sys_file"

    parent_id: Mapped[UUID] = mapped_column(
        ForeignKey("sys_file.id", ondelete="CASCADE"),
        nullable=True,
        comment="文件 ID",
    )
    created_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("sys_user.id", ondelete="SET NULL"),
        nullable=True,
        comment="創建人ID",
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件名稱")
    location: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="文件位置"
    )
    size: Mapped[int] = mapped_column(
        BigInteger, default=0, nullable=False, comment="文件大小"
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False, comment="文件類型")
    storage_type: Mapped[StorageTypeEnum] = mapped_column(
        Enum(StorageTypeEnum),
        default=StorageTypeEnum.LOCAL,
        nullable=False,
        comment="文件來源",
    )
