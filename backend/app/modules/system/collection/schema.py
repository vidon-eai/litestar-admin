from uuid import UUID

from app.core.base_schema import BaseSchema
from pydantic import BaseModel, Field


class CollectionBase(BaseSchema):
    dataset_id: UUID = Field(..., description="知識庫關聯ID")
    name: str = Field(..., description="數據集名稱")


class CollectionCreate(BaseModel):
    dataset_id: UUID = Field(..., description="知識庫關聯ID")
    name: str = Field(..., description="數據集名稱")


class CollectionUpdate(BaseModel):
    dataset_id: UUID = Field(..., description="知識庫關聯ID")
    name: str | None = Field(None, description="數據集名稱")


class CollectionRead(CollectionBase): ...
