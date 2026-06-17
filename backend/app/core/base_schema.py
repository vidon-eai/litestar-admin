from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from pydantic import model_validator

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None, description="Primary Key")
    created_at: datetime = Field(..., description="Create record datetime")
    updated_at: datetime = Field(..., description="Update record datetime")


    @model_validator(mode="after")
    def move_fields_to_end(self) -> "BaseSchema":
        d = self.__dict__
        sort_fields = ["created_at", "updated_at"]
        for field in sort_fields:
            if field in d:
                val = d.pop(field)
                d[field] = val
        return self