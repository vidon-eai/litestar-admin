from typing import Any
from advanced_alchemy.exceptions import DuplicateKeyError, IntegrityError, NotFoundError
from litestar import Response
from litestar.exceptions import ValidationException
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.common.constant import RET, MySQLError, PostgreSQLError
from app.common.response import ErrorResponse, ResponseSchema

from app.config.setting import app_setting


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

    if isinstance(exc, (IntegrityError, ProgrammingError, OperationalError)):
        original_cause = getattr(exc, "__cause__", None)

        if original_cause and hasattr(original_cause, "orig") and original_cause.orig:
            orig_err = original_cause.orig

            # ==================== PostgreSQL 異常處理分支 ====================
            if app_setting.DB_TYPE == "postgresql":
                # asyncpg 驅動的錯誤碼欄位通常是 sqlstate，某些驅動是 pgcode
                pg_code = getattr(orig_err, "sqlstate", None) or getattr(
                    orig_err, "pgcode", None
                )
                print(f"Extracted PostgreSQL error code: {pg_code}")  # 調試輸出
                # 如果屬性裡都拿不到，嘗試從 args 中抓取 5 碼的 SQLSTATE 字串
                if not pg_code and hasattr(orig_err, "args") and orig_err.args:
                    raw_code = str(orig_err.args[0])
                    if len(raw_code) == 5:
                        pg_code = raw_code

                if pg_code:
                    try:
                        db_error = PostgreSQLError.get(str(pg_code))
                    except ValueError:
                        db_error = PostgreSQLError.get(
                            PostgreSQLError.ER_UNKNOWN_ERROR.code
                        )
                    code = db_error.code
                    detail = db_error.msg
                else:
                    # 讀取不到 code 時的 fallback
                    code = RET.DB_ERR.code
                    detail = f"PostgreSQL 錯誤: {str(orig_err)}"

            # ==================== MySQL 異常處理分支 ====================
            elif app_setting.DB_TYPE == "mysql":
                if hasattr(orig_err, "args") and orig_err.args:
                    raw_code = orig_err.args[0]
                    try:
                        db_error = MySQLError.get(int(raw_code))
                    except (ValueError, TypeError):
                        db_error = MySQLError.get(MySQLError.ER_UNKNOWN_ERROR.code)
                    code = db_error.code
                    detail = db_error.msg
                else:
                    code = RET.DB_ERR.code
                    detail = RET.DB_ERR.msg

            # ==================== 其他資料庫 (如 SQLite) ====================
            else:
                code = RET.DB_ERR.code
                detail = str(orig_err)

    elif isinstance(exc, NotFoundError):
        status_code = RET.NOT_FOUND.code
        detail = detail or RET.NOT_FOUND.msg

    elif isinstance(exc, DuplicateKeyError):
        status_code = RET.CONFLICT.code
        detail = RET.CONFLICT.msg

    elif isinstance(exc, ValidationException):
        status_code = RET.BAD_REQUEST.code
        detail = extra_data

    # 4. 構建並回傳回應
    content = ErrorResponse(
        code=code,
        status_code=status_code,
        detail=detail,
        is_success=False,
    )
    return Response(
        content=content,
        status_code=status_code,
    )
