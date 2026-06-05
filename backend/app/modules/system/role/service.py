from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.db.models.models import Role


class RoleService(SQLAlchemyAsyncRepositoryService[Role]):

    class Repo(SQLAlchemyAsyncRepository[Role]):
        model_type = Role

    repository_type = Repo