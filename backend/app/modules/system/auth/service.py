import hashlib
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from litestar.exceptions import NotFoundException, PermissionDeniedException
from sqlalchemy.orm.strategy_options import undefer_group
from app.db.models.models import Account


class AuthService(SQLAlchemyAsyncRepositoryService[Account]):

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
            msg = "帳戶或密碼錯誤"
            raise PermissionDeniedException(detail=msg)

        return account
