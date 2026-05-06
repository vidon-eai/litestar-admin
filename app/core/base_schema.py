from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None, description="Primary Key")
    created_time: datetime | None = Field(default=None, description="Create record datetime")
    updated_time: datetime | None = Field(default=None, description="Update record datetime")