from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
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


UserDTO = SQLAlchemyDTO[User]

class UserReadDTO(UserDTO):
    config = SQLAlchemyDTOConfig()


class UserCreateDTO(UserDTO):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at"},  # 排除自動生成的欄位
        max_nested_depth=1,
    )


class UserUpdateDTO(UserDTO):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at"},
        partial=True,
        max_nested_depth=1,
    )
