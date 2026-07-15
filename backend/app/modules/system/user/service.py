from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import (
    SQLAlchemyAsyncRepositoryService,
)
from app.db.models import User


class UserService(SQLAlchemyAsyncRepositoryService[User]):
    class Repo(SQLAlchemyAsyncRepository[User]):
        model_type = User

    repository_type = Repo
