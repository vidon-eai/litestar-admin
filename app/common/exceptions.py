
from typing import Any
from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar import Response
from litestar.exceptions import ValidationException
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

from app.common.constant import RET
from app.common.response import ResponseSchema


def unified_exception_handler(request: Any, exc: Exception) -> Response:
    """
    全域異常處理器：
    1. 增加 Timestamp 記錄。
    2. 安全地提取 HTTPException 中的 detail 與 extra。
    3. 統一回傳 ErrorResponse 結構。
    """
    # 1. 取得狀態碼與錯誤訊息
    code = RET.EXCEPTION.code
    status_code = getattr(exc, "status_code", RET.INTERNAL_SERVER_ERROR.code)
    detail = getattr(exc, "detail", RET.INTERNAL_SERVER_ERROR.msg)
    # 2. 安全取得 extra (Litestar 的 HTTPException 通常有 extra 屬性)
    # 使用 getattr 並提供預設值，避免產生 AttributeError
    extra_data = getattr(exc, "extra", None)
    if isinstance(exc, NotFoundError):
        status_code = RET.NOT_FOUND.code
        detail = RET.NOT_FOUND.msg
    elif isinstance(exc, DuplicateKeyError):
        status_code = RET.CONFLICT.code
        detail = RET.CONFLICT.msg
    elif isinstance(exc, ValidationException):
        status_code = RET.BAD_REQUEST.code
        detail = extra_data
   

    # 4. 構建並回傳回應
    content = ResponseSchema(
        code=code,
        status_code=status_code,
        detail=detail,
        is_success=False,
    ).model_dump()
    
    return Response(
        content=content,
        status_code=status_code,
    )