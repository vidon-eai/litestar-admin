from tkinter import N
from litestar import Request
from litestar.enums import ScopeType
from litestar.middleware import ASGIMiddleware
from litestar.types import ASGIApp, Message, Receive, Scope, Send
import json

from app.config.setting import app_setting
from app.modules.system.audit_log.schema import AuditLogCreate
from app.modules.system.audit_log.service import AuditLogService
from urllib.parse import parse_qs


class AuditLogMiddleware(ASGIMiddleware):
    scopes = [ScopeType.HTTP]
    exclude_path_pattern = ["/api/v1/schema/*", "/api/v1/auth/logout"]

    async def handle(
        self, scope: Scope, receive: Receive, send: Send, next_app: ASGIApp
    ) -> None:

        request = Request(scope)
        request_ip = request.client.host if request.client else "unknown"

        headers_dict = dict(scope.get("headers", []))
        content_type = headers_dict.get(b"content-type", b"").decode("utf-8")


        cached_request_body = b""
        response_body_bytes = b""
        status_code = None

        async def wrapped_receive() -> dict:
            nonlocal cached_request_body
            message = await receive()
            if message["type"] == "http.request":
                cached_request_body += message.get("body", b"")
            return message

        async def wrapped_send(message: Message) -> None:
            nonlocal status_code, response_body_bytes
            if message["type"] == "http.response.start":
                status_code = message["status"]
            elif message["type"] == "http.response.body":
                response_body_bytes += message.get("body", b"")

            await send(message)

        try:
            await next_app(scope, wrapped_receive, wrapped_send)
        finally:
            if not hasattr(request, "user") or request.user is None:
                return

            payload = None

            if cached_request_body:
                body_str = cached_request_body.decode("utf-8", errors="ignore")

                if "application/x-www-form-urlencoded" in content_type:
                    parsed = parse_qs(body_str)
                    payload = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

                elif "application/json" in content_type:
                    try:
                        payload = json.loads(body_str)
                    except Exception:
                        payload = {"raw": body_str}
                else:
                    payload = {"raw": body_str}
                    
            body_json = None
            if response_body_bytes:
                try:
                    body_json = json.loads(response_body_bytes.decode("utf-8"))
                except Exception:
                    body_json = {"raw": "Non-JSON or dynamic stream response"}


            async with app_setting.DB_CONFIG.get_session() as db_session:
                audit_log_service = AuditLogService(db_session)
                data = AuditLogCreate(
                    user_id=request.user.id,
                    request_method=request.method,
                    request_path=str(f"{request.url.path}{('?' + request.url.query) if request.url.query else ''}"),
                    request_payload=payload,
                    request_ip=request_ip,
                    status_code=status_code,
                    response_body=body_json,
                )
                await audit_log_service.create(data=data, auto_commit=True)
