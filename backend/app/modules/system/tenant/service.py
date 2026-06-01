from advanced_alchemy.service import (
    SQLAlchemyAsyncRepositoryService,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.db.models.models import Tenant

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService


class TenantService(SQLAlchemyAsyncRepositoryService[Tenant]):

    class Repo(SQLAlchemyAsyncRepository[Tenant]):
        model_type = Tenant

    repository_type = Repo
