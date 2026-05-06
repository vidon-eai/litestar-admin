from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import Base

if TYPE_CHECKING:
    from app.modules.system.user.model import User


class Post(Base):
    __tablename__ = "posts"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="作者（使用者 ID）",
    )
    title: Mapped[str] = mapped_column(String(255), nullable=True, comment="Title")
    content: Mapped[str] = mapped_column(Text, nullable=True, comment="Content")

    is_publish: Mapped[bool] = mapped_column(Boolean, default=False, comment="Publish")

    user: Mapped["User"] = relationship(
        back_populates="posts", lazy="joined", innerjoin=True, viewonly=True
    )
