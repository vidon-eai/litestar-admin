from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from app.db.models import {pascal_name}


class {pascal_name}Service(SQLAlchemyAsyncRepositoryService[{pascal_name}]):
    class Repo(SQLAlchemyAsyncRepository[{pascal_name}]):
        model_type = {pascal_name}

    repository_type = Repo