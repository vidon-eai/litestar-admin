from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, TypeVar

from app.common.constant import RET
from litestar.openapi.datastructures import ResponseSpec
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

T = TypeVar("T")


@dataclass(kw_only=True)
class ApiResponse(Generic[T]):
    code: int | str = RET.OK.code
    status_code: int = HTTP_200_OK
    data: T | None
    is_success: bool = True
    detail: str | list[Any] | None | Any = RET.OK.msg
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(kw_only=True)
class ErrorResponse(ApiResponse):
    code: int | str = RET.INTERNAL_SERVER_ERROR.code
    status_code: int = HTTP_500_INTERNAL_SERVER_ERROR
    data: None = None
    is_success: bool = False
    detail: str | list[Any] | None | Any = RET.INTERNAL_SERVER_ERROR.msg


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
