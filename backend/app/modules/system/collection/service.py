from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from app.db.models import Collection


class CollectionService(SQLAlchemyAsyncRepositoryService[Collection]):
    class Repo(SQLAlchemyAsyncRepository[Collection]):
        model_type = Collection

    repository_type = Repo
