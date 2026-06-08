from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.core.base_schema import BaseSchema


class AuditLogBase(BaseSchema):
    user_id: UUID = Field(..., description="用戶ID")
    request_path: str | None = Field(None, description="請求路徑")
    request_method: str | None = Field(None, description="請求方法")
    request_payload_before: dict | None = Field(None, description="請求內容(變更前)")
    request_payload_after: dict | None = Field(None, description="請求內容(變更後)")
    request_ip: str | None = Field(None, description="請求ID")
    status_code: int | None = Field(None, description="狀態碼")
    response_body: dict | None = Field(None, description="回應內容")
    process_time: datetime | None = Field(None, description="處理時間")

class AuditLogCreate(BaseModel):
    user_id: UUID = Field(..., description="用戶ID")
    request_path: str | None = Field(None, description="請求路徑")
    request_method: str = Field(description="請求方法")
    request_payload_before: dict | None = Field(None, description="請求內容(變更前)")
    request_payload_after: dict | None = Field(None, description="請求內容(變更後)")
    request_ip: str | None = Field(None, description="請求ID")
    status_code: int | None = Field(None, description="狀態碼")
    response_body: dict | None = Field(None, description="回應內容")
    process_time: datetime | None = Field(None, description="處理時間")


class AuditLogUpdate(BaseModel):
    pass


class AuditLogRead(AuditLogBase):
    pass
