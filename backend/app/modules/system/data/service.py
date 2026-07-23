from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from app.db.models import Data


class DataService(SQLAlchemyAsyncRepositoryService[Data]):
    class Repo(SQLAlchemyAsyncRepository[Data]):
        model_type = Data

    repository_type = Repo
