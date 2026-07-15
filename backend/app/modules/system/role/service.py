from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from app.db.models import Role


class RoleService(SQLAlchemyAsyncRepositoryService[Role]):
    class Repo(SQLAlchemyAsyncRepository[Role]):
        model_type = Role

    repository_type = Repo
