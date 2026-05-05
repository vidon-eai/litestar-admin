from typing import Any
from advanced_alchemy.exceptions import DuplicateKeyError, IntegrityError, NotFoundError
from litestar import Request, Response
from litestar import status_codes
from litestar.exceptions import ValidationException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.common.constant import RET
from app.common.response import ResponseSchema


def unified_exception_handler(request: Any, exc: Exception) -> Response:
    """
    全域異常處理器：
    1. 增加 Timestamp 記錄。
    2. 安全地提取 HTTPException 中的 detail 與 extra。
    3. 統一回傳 ErrorResponse 結構。
    """
    code = RET.EXCEPTION.code
    status_code = getattr(exc, "status_code", RET.INTERNAL_SERVER_ERROR.code)
    detail = getattr(exc, "detail", RET.INTERNAL_SERVER_ERROR.msg)
    extra_data = getattr(exc, "extra", None)
    if isinstance(exc, IntegrityError):
        original_cause = getattr(exc, "__cause__", None)
        
        if original_cause and hasattr(original_cause, "orig"):
            code = str(original_cause.orig.args[0])
            detail = str(original_cause.orig.args[1]) 
        elif original_cause:
            detail = str(original_cause)
            
        status_code = HTTP_500_INTERNAL_SERVER_ERROR
        code = RET.DB_ERR.code
    
    elif isinstance(exc, NotFoundError):
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


def sqlalchemy_exception_handler(request, exc: Exception) -> Response:
    # 這裡可以記錄日誌
    print(f"Detected DB Error: {exc}")

    return Response(
        content={
            "error": "Database Connection Failed",
            "message": "無法連接到資料庫，請檢查數據庫服務狀態及端口(3307)是否正確。",
        },
        status_code=status_codes.HTTP_503_SERVICE_UNAVAILABLE,
    )
