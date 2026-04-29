from datetime import date, datetime
from sqlalchemy import Boolean, Date, String, null
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime
from app.core.base_model import Base


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, comment="Username"
    )
    email: Mapped[str | None] = mapped_column(
        String(64), nullable=True, unique=True, comment="Email address"
    )

    description: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="Description"
    )

    phone: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="Phone"
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
