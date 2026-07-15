from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from app.db.models import File


class FileService(SQLAlchemyAsyncRepositoryService[File]):
    class Repo(SQLAlchemyAsyncRepository[File]):
        model_type = File

    repository_type = Repo

    def get_storage(self, state):
        return state.storage
