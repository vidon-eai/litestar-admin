from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from app.common.enums import StorageTypeEnum
from app.db.models.dataset import Collection
from sqlalchemy import (
    BigInteger,
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


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
    collections: Mapped[list["Collection"]] = relationship(
        "Collection",
        back_populates="file",
        cascade="all, delete-orphan",
    )
