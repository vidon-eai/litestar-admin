from uuid import UUID

from app.core.base_schema import BaseSchema
from app.modules.system.collection.schema import CollectionRead
from pydantic import BaseModel, Field


class DatasetBase(BaseSchema):
    created_by: UUID = Field(..., description="創建人ID")
    updated_by: UUID | None = Field(None, description="更新人ID")
    name: str = Field(..., description="知識庫名稱")
    description: str | None = Field(None, description="知識庫描述")


class DatasetCreate(BaseModel):
    created_by: UUID | None = Field(None, description="創建人ID")
    name: str = Field(..., description="知識庫名稱")
    description: str | None = Field(None, description="知識庫描述")


class DatasetUpdate(BaseModel):
    name: str | None = Field(None, description="知識庫名稱")
    description: str | None = Field(None, description="知識庫描述")


class DatasetRead(DatasetBase): ...


class DatesetWithCollectionsRead(DatasetBase):
    collections: list[CollectionRead] = Field([])
