from uuid import UUID

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column


class UserMixin:
    created_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("sys_user.id", ondelete="SET NULL"),
        default=None,
        nullable=True,
        comment="創建人ID",
    )
    updated_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("sys_user.id", ondelete="SET NULL"),
        default=None,
        nullable=True,
        comment="更新人ID",
    )
