from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from app.db.models.base_model import UserMixin
from sqlalchemy import TEXT, ForeignKey, String
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column, relationship

LongText = TEXT().with_variant(mysql.LONGTEXT(), "mysql", "mariadb")


# class LongText(TypeDecorator[str | None]):
#     impl = TEXT
#     cache_ok = True

#     def process_bind_param(self, value: str | None, dialect: Dialect) -> str | None:
#         if value is None:
#             return value
#         return value

#     def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]:
#         if dialect.name == "postgresql":
#             return dialect.type_descriptor(TEXT())
#         elif dialect.name == "mysql":
#             return dialect.type_descriptor(LONGTEXT())
#         else:
#             return dialect.type_descriptor(TEXT())

#     def process_result_value(self, value: str | None, dialect: Dialect) -> str | None:
#         if value is None:
#             return value
#         return value


TABLE_PREFIX = "rag"


if TYPE_CHECKING:
    from app.db.models import File


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
    question: Mapped[str | None] = mapped_column(LongText, default=None, nullable=True)
    answer: Mapped[str | None] = mapped_column(LongText, default=None, nullable=True)

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="datas")
    collection: Mapped["Collection"] = relationship(
        "Collection", back_populates="datas"
    )
