from advanced_alchemy.service import (
    SQLAlchemyAsyncRepositoryService,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.db.models.models import User


class UserService(SQLAlchemyAsyncRepositoryService[User]):
    class Repo(SQLAlchemyAsyncRepository[User]):
        model_type = User

    repository_type = Repo