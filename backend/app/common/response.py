from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, TypeVar

from app.common.constant import RET
from litestar import Response
from litestar.openapi.datastructures import ResponseSpec
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from pydantic import BaseModel, Field

T = TypeVar("T")


@dataclass(kw_only=True)
class BaseRespose(Generic[T]):
    code: int | str = RET.OK.code
    status_code: int = HTTP_200_OK
    is_success: bool = True
    detail: str | list[Any] | None | Any = RET.OK.msg
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(kw_only=True)
class ApiResponse(Generic[T]):
    data: T | None


@dataclass
class PaginationResponse(BaseRespose[T]):
    data: list[T]
    total: int
    limit: int
    offset: int


@dataclass(kw_only=True)
class ErrorResponse(ApiResponse):
    code: int | str = RET.INTERNAL_SERVER_ERROR.code
    status_code: int = HTTP_500_INTERNAL_SERVER_ERROR
    data: None = None
    is_success: bool = False
    detail: str | list[Any] | None | Any = RET.INTERNAL_SERVER_ERROR.msg


class ResponseSchema(BaseModel, Generic[T]):
    """統一錯誤回應模型"""

    code: int | str = Field(..., description="業務狀態碼")
    status_code: int = Field(..., description="HTTP狀態碼")
    data: T | None = Field(default=None, description="回應數據")
    detail: str | list[Any] = Field(..., description="詳情說明")
    is_success: bool = Field(default=False, description="操作是否成功")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now().astimezone(),
        description="回應時間",
    )


class SuccessResponse(Response[ResponseSchema[T]], Generic[T]):
    def __init__(
        self, data: T, detail: str = RET.OK.msg, biz_code: int = RET.OK.code, **kwargs
    ):
        status_code = kwargs.get("status_code", 200)
        content = ResponseSchema(
            code=biz_code,
            status_code=status_code,
            data=data,
            detail=detail,
            is_success=200 <= status_code < 300,
        )
        super().__init__(content=content, **kwargs)


COMMON_RESPONSES: dict[int, ResponseSpec] = {
    HTTP_400_BAD_REQUEST: ResponseSpec(
        data_container=ErrorResponse,
        description="請求參數錯誤",
        generate_examples=False,
    ),
    HTTP_401_UNAUTHORIZED: ResponseSpec(
        data_container=ErrorResponse,
        description="未授權",
    ),
    HTTP_404_NOT_FOUND: ResponseSpec(
        data_container=ErrorResponse,
        description="資源不存在",
        generate_examples=False,
    ),
    HTTP_500_INTERNAL_SERVER_ERROR: ResponseSpec(
        data_container=ErrorResponse,
        description="伺服器內部錯誤",
        generate_examples=False,
    ),
}
