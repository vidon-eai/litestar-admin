from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from app.db.models.base_model import UserMixin
from sqlalchemy import TEXT, ForeignKey, String
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column, relationship

# 相容性文字型態設定：
# - PostgreSQL / SQLite：使用標準 TEXT（PostgreSQL TEXT 可支援高達 1GB 文字）
# - MySQL / MariaDB：改用 LONGTEXT 以突破標準 TEXT 約 64KB 的儲存上限，避免長文本溢位
LongText = TEXT().with_variant(mysql.LONGTEXT(), "mysql", "mariadb")

TABLE_PREFIX = "rag"


if TYPE_CHECKING:
    from app.db.models import File


class VectorIndexMixin:
    vector_index_prefix: str = "Vector_index"
    vector_index_suffix: str = "Node"

    @property
    def vector_index_name(self) -> str:
        raw_id = getattr(self, "dataset_id", None) or getattr(self, "id", None)
        if not raw_id:
            return ""
        formatted_id = str(raw_id).replace("-", "_")
        return f"{self.vector_index_prefix}_{formatted_id}_{self.vector_index_suffix}"


class Dataset(UUIDv7AuditBase, UserMixin, VectorIndexMixin):
    __tablename__ = f"{TABLE_PREFIX}_dataset"

    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="知識庫名")
    description: Mapped[str | None] = mapped_column(
        String(255), default=None, nullable=True, comment="知識庫描述"
    )

    # embedding_model: Mapped[str] = mapped_column(
    #     String(255), nullable=True, comment="Embedding模型"
    # )
    # embedding_model_provider: Mapped[str] = mapped_column(
    #     String(255), nullable=True, comment="Embedding模型供應商"
    # )

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


class Collection(UUIDv7AuditBase, UserMixin, VectorIndexMixin):
    __tablename__ = f"{TABLE_PREFIX}_collection"

    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{TABLE_PREFIX}_dataset.id", ondelete="CASCADE"),
        nullable=False,
    )

    file_id: Mapped[UUID] = mapped_column(
        ForeignKey("sys_file.id", ondelete="CASCADE"),
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
        lazy="selectin",
    )

    file: Mapped["File"] = relationship(
        "File", back_populates="collections", lazy="selectin"
    )


class Data(UUIDv7AuditBase, UserMixin, VectorIndexMixin):
    __tablename__ = f"{TABLE_PREFIX}_data"

    dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{TABLE_PREFIX}_dataset.id", ondelete="CASCADE"),
        nullable=False,
    )
    collection_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{TABLE_PREFIX}_collection.id", ondelete="CASCADE"),
        nullable=False,
    )
    question: Mapped[str | None] = mapped_column(LongText, default=None, nullable=True)
    answer: Mapped[str | None] = mapped_column(LongText, default=None, nullable=True)

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="datas")
    collection: Mapped["Collection"] = relationship(
        "Collection", back_populates="datas"
    )
