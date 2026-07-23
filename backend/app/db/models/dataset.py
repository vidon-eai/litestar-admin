from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from app.db.models.base_model import UserMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

TABLE_PREFIX = "rag"


class Dataset(UUIDv7AuditBase, UserMixin):
    __tablename__ = f"{TABLE_PREFIX}_dataset"

    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="知識庫名")
    description: Mapped[str | None] = mapped_column(
        String(255), default=None, nullable=True, comment="知識庫描述"
    )

    collections: Mapped[list["Collection"]] = relationship(
        "Collection",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )
    datas: Mapped[list["Data"]] = relationship(
        "Data",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )


class Collection(UUIDv7AuditBase, UserMixin):
    __tablename__ = f"{TABLE_PREFIX}_collection"

    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{TABLE_PREFIX}_dataset.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    dataset: Mapped["Dataset"] = relationship(
        "Dataset", back_populates="collections", lazy="selectin"
    )
    datas: Mapped[list["Data"]] = relationship(
        "Data",
        back_populates="collection",
        cascade="all, delete-orphan",
    )


class Data(UUIDv7AuditBase, UserMixin):
    __tablename__ = f"{TABLE_PREFIX}_data"

    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{TABLE_PREFIX}_dataset.id", ondelete="CASCADE"),
        nullable=False,
    )
    collection_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{TABLE_PREFIX}_collection.id", ondelete="CASCADE"),
        nullable=False,
    )
    question: Mapped[str | None] = mapped_column(
        String(255), default=None, nullable=True
    )
    answer: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="datas")
    collection: Mapped["Collection"] = relationship(
        "Collection", back_populates="datas"
    )
