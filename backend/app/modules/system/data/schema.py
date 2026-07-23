from uuid import UUID

from app.core.base_schema import BaseSchema
from pydantic import BaseModel, Field


class DataBase(BaseSchema):
    dataset_id: UUID = Field(...)
    collection_id: UUID = Field(...)
    question: str = Field(...)
    answer: str | None = Field(None)


class DataCreate(BaseModel):
    dataset_id: UUID = Field(...)
    collection_id: UUID = Field(...)
    question: str = Field(...)
    answer: str | None = Field(None)


class DataUpdate(BaseModel):
    question: str = Field(...)
    answer: str | None = Field(None)


class DataRead(DataBase): ...
