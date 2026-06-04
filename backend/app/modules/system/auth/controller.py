from typing import Annotated, Any
from advanced_alchemy.extensions.litestar import providers
from litestar import Controller, Request, Response, get, post
from litestar.enums import RequestEncodingType
from litestar.params import Body
from pydantic import BaseModel

from app.common.response import ApiResponse
from app.core.guards import auth
from app.db.models.models import Account
from app.modules.system.account.schema import AccountRead
from app.modules.system.auth.service import AuthService


class AccountLogin(BaseModel):
    username: str
    password: str


class AuthController(Controller):
    path = "/auth"
    tags = ["驗證管理模塊"]

    dependencies = {
        **providers.create_service_dependencies(
            AuthService,
            "auth_service",
        )
    }

    @post("/login")
    async def login(
        self,
        data: Annotated[
            AccountLogin,
            Body(title="OAuth2 Login", media_type=RequestEncodingType.URL_ENCODED),
        ],
        auth_service: AuthService,
    ) -> Response[Any]:

        account = await auth_service.authenticate(data.username, data.password)

        return auth.login(
            identifier=account.username,
        )

    @get("/me")
    async def get_me(
        self, auth_service: AuthService, current_user: Account
    ) -> ApiResponse[AccountRead]:

        return ApiResponse(
            data=auth_service.to_schema(current_user, schema_type=AccountRead),
            detail="取得當前用戶成功",
        )

    @post("/logout")
    async def logout(self, request: Request) -> Response[Any]:

        request.cookies.pop(auth.key, None)
        request.clear_session()
        response = Response(
            content=ApiResponse(detail="登出成功", data=None), status_code=200
        )
        response.delete_cookie(auth.key)

        return response
