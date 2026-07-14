from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class Dataset(UUIDv7AuditBase):
    __tablename__ = "rag_datasets"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    intro: Mapped[str] = mapped_column(String(1000), default="")

    created_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("sys_user.id", ondelete="SET NULL"),
        nullable=True,
        comment="創建人ID",
    )
