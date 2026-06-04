from __future__ import annotations
import hashlib
from typing import TYPE_CHECKING
from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.service import (
    SQLAlchemyAsyncRepositoryService,
    schema_dump,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from litestar.exceptions import NotFoundException, PermissionDeniedException
from sqlalchemy.orm.strategy_options import undefer_group
from app.db.models.models import Account

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

if TYPE_CHECKING:
    from advanced_alchemy.service import ModelDictT


class AccountService(SQLAlchemyAsyncRepositoryService[Account]):

    class Repo(SQLAlchemyAsyncRepository[Account]):
        model_type = Account

    repository_type = Repo

    async def authenticate(self, username: str, password: str) -> Account:

        account = await self.get_one_or_none(
            username=username, load=[undefer_group("security_sensitive")]
        )
        if not account:
            raise NotFoundException(detail="找不到該用戶")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if hashed_password != account.hashed_password:
            msg = "User not found or password invalid"
            raise PermissionDeniedException(detail=msg)

        return account
