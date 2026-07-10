from uuid import UUID

from app.core.base_schema import BaseSchema
from pydantic import BaseModel, Field


class AuditLogBase(BaseSchema):
    user_id: UUID = Field(..., description="用戶ID")
    request_method: str = Field(description="請求方法")
    request_path: str | None = Field(None, description="請求路徑")
    request_payload: dict | None = Field(None, description="請求內容")
    request_ip: str | None = Field(None, description="請求ID")
    status_code: int | None = Field(None, description="狀態碼")
    response_body: dict | None = Field(None, description="回應內容")


class AuditLogCreate(BaseModel):
    user_id: UUID = Field(..., description="用戶ID")
    request_method: str = Field(description="請求方法")
    request_path: str | None = Field(None, description="請求路徑")
    request_payload: dict | None = Field(None, description="請求內容")
    request_ip: str | None = Field(None, description="請求ID")
    status_code: int | None = Field(None, description="狀態碼")
    response_body: dict | None = Field(None, description="回應內容")

