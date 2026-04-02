from litestar import MediaType, Request, Response
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from src.common.response import UnifiedResponse


def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    """处理 HTTP 异常 (如 404, 400, 500 等)"""

    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    detail = getattr(exc, "detail", "")

    return Response(
        media_type=MediaType.JSON,
        content=UnifiedResponse.error(
            msg=detail, code=status_code, status_code=status_code
        ).model_dump(),
        status_code=status_code,
    )


async def general_exception_handler(
    request: Request, exc: Exception
) -> UnifiedResponse:
    """处理未捕获的通用异常"""
    # 生产环境建议记录日志，不要直接返回原始错误信息
    return UnifiedResponse.error(
        msg="Internal Server Error",
        code=HTTP_500_INTERNAL_SERVER_ERROR,
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )
