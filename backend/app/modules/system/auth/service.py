from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from app.db.models.models import User
from litestar.exceptions import NotFoundException, PermissionDeniedException
from sqlalchemy.orm.strategy_options import undefer_group


class AuthService(SQLAlchemyAsyncRepositoryService[User]):

    class Repo(SQLAlchemyAsyncRepository[User]):
        model_type = User

    repository_type = Repo

    async def authenticate(self, username: str, password: str) -> User:

        user = await self.get_one_or_none(
            username=username, load=[undefer_group("security_sensitive")]
        )
        if not user:
            raise NotFoundException(detail="找不到該用戶")


        if not user.password.verify(password):
            msg = "帳戶或密碼錯誤"
            raise PermissionDeniedException(detail=msg)

        return user
