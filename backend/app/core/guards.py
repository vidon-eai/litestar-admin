from __future__ import annotations
from datetime import timedelta
from typing import TYPE_CHECKING
from litestar.security.jwt import OAuth2PasswordBearerAuth, Token
from app.db.models.models import Account

from app.modules.system.account.service import AccountService
from app.config.setting import app_setting

if TYPE_CHECKING:
    from typing import Any
    from litestar.connection import ASGIConnection


async def retrieve_user_handler(
    token: Token, connection: ASGIConnection[Any, Any, Any, Any]
) -> Account | None:

    async with app_setting.DB_CONFIG.get_session() as db_session:

        account_service = AccountService(session=db_session)

        account = await account_service.get_one_or_none(username=token.sub)

        if not account:
            return None

        return account


ACCESS_TOKEN_EXPIRATION = timedelta(minutes=15)


auth = OAuth2PasswordBearerAuth[Account](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=app_setting.SECRET_KEY,
    default_token_expiration=ACCESS_TOKEN_EXPIRATION,
    token_url="/api/v1/auth/login",
    exclude=["^/api/v1/schema", "/api/v1/auth/login", "/api/v1/auth/logout"],
)
