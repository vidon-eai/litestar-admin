from pydantic import BaseModel, Field
from uuid import UUID
from app.core.base_schema import BaseSchema


class FileBase(BaseSchema):
    parent_id: UUID | None = Field(None, description="文件 ID")
    created_by: UUID | None = Field(None, description="創建人ID")
    name: str = Field(..., description="文件名稱")
    location: str = Field(..., description="文件位置")
    size: int = Field(0, description="文件大小")
    type: str = Field(..., description="文件類型")
    source_type: str = Field("LOCAL", description="文件來源")
    created_by: UUID | None = Field(None, description="創建人ID")
    name: str = Field(..., description="文件名稱")
    location: str = Field(..., description="文件位置")
    size: int = Field(0, description="文件大小")
    type: str = Field(..., description="文件類型")
    source_type: str = Field("LOCAL", description="文件來源")


class FileCreate(BaseModel):
    created_by: UUID | None = Field(None, description="創建人ID")
    name: str = Field(..., description="文件名稱")
    location: str = Field(..., description="文件位置")
    size: int = Field(0, description="文件大小")
    type: str = Field(..., description="文件類型")
    source_type: str = Field("LOCAL", description="文件來源")
    created_by: UUID | None = Field(None, description="創建人ID")
    name: str = Field(..., description="文件名稱")
    location: str = Field(..., description="文件位置")
    size: int = Field(0, description="文件大小")
    type: str = Field(..., description="文件類型")
    source_type: str = Field("LOCAL", description="文件來源")


class FileUpdate(BaseModel):
    ...


class FileRead(FileBase):
    ...
