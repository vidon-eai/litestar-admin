from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db.models import AuditLog


class AuditLogService(SQLAlchemyAsyncRepositoryService[AuditLog]):
    class Repo(SQLAlchemyAsyncRepository[AuditLog]):
        model_type = AuditLog

    repository_type = Repo
