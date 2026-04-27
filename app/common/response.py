from datetime import datetime
from typing import Any, Generic
from litestar import Response, status_codes
from litestar.openapi.datastructures import ResponseSpec
from pydantic import BaseModel, Field
from pydantic.types import T

from app.common.constant import RET


class ResponseSchema(BaseModel, Generic[T]):
    """統一錯誤回應模型"""
    code: int = Field(..., description="業務狀態碼")
    status_code: int = Field(..., description="HTTP狀態碼")
    data: T | None = Field(default=None, description="响应数据")
    detail: str | list[Any] = Field(..., description="詳情說明")
    is_success: bool = Field(default=False, description="操作是否成功")
    timestamp: str = Field(
        default=datetime.now().isoformat(),
        description="回應時間"
    )

class SuccessResponse(Response[T]):
    def __init__(self, data: T, detail: str = RET.OK.msg, biz_code: int = RET.OK.code, **kwargs):
        status_code = kwargs.get("status_code", 200)
        content = ResponseSchema(
            code=biz_code,
            status_code=status_code,
            data=data,
            detail=detail,
            is_success=200 <= status_code < 300,
            timestamp=datetime.now().isoformat()
        ).model_dump()
        super().__init__(content=content, **kwargs)
        
        
        



COMMON_RESPONSES: dict[int, ResponseSpec] = {
    status_codes.HTTP_400_BAD_REQUEST: ResponseSpec(data_container=ResponseSchema[None], description="請求參數錯誤", generate_examples=False),
    status_codes.HTTP_401_UNAUTHORIZED: ResponseSpec(data_container=ResponseSchema[None], description="未授權",),
    status_codes.HTTP_404_NOT_FOUND: ResponseSpec(data_container=ResponseSchema[None], description="資源不存在", generate_examples=False),
    status_codes.HTTP_500_INTERNAL_SERVER_ERROR: ResponseSpec(data_container=ResponseSchema[None], description="伺服器內部錯誤", generate_examples=False),
}