
from datetime import date
from uuid import UUID
from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import Boolean, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


# class Base(UUIDv7AuditBase):
#     __abstract__ = True
    
class User(UUIDv7AuditBase):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, comment="用戶名"
    )
    email: Mapped[str | None] = mapped_column(
        String(64), nullable=True, unique=True, comment="電子郵箱"
    )

    description: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="描述"
    )

    phone: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="電話號碼"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否啟用"
    )

    dob: Mapped[date] = mapped_column(
        Date, default=None, nullable=True, comment="出生日期"
    )

    address: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="地址"
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=True
    )
    
    
class Post(UUIDv7AuditBase):
    __tablename__ = "posts"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="作者（使用者 ID）",
    )
    title: Mapped[str] = mapped_column(String(255), nullable=True, comment="帖子標題")
    content: Mapped[str] = mapped_column(Text, nullable=True, comment="帖子內容")

    is_publish: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否發佈")


    description: Mapped[str] = mapped_column(String(255), nullable=True, comment="帖子描述")

    user: Mapped["User"] = relationship(
        back_populates="posts", lazy="joined", innerjoin=True, viewonly=True
    )