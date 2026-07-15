from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from app.db.models.base_model import UserMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

TABLE_PREFIX = "rag"


class Dataset(UUIDv7AuditBase, UserMixin):
    __tablename__ = f"{TABLE_PREFIX}_dataset"

    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="知識庫名")
    description: Mapped[str | None] = mapped_column(
        String(255), default=None, nullable=True, comment="知識庫描述"
    )


class Collection(UUIDv7AuditBase, UserMixin):
    __tablename__ = f"{TABLE_PREFIX}_collection"

    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{TABLE_PREFIX}_dataset.id", ondelete="cascade"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)


class Data(UUIDv7AuditBase, UserMixin):
    __tablename__ = f"{TABLE_PREFIX}_data"
    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{TABLE_PREFIX}_dataset.id", ondelete="cascade"),
        nullable=False,
    )
    collection_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{TABLE_PREFIX}_collection.id", ondelete="cascade"),
        nullable=False,
    )
    question: Mapped[str | None] = mapped_column(
        String(255), default=None, nullable=True
    )
    answer: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)
