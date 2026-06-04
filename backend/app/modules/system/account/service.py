from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.db.models.models import Account


class AccountService(SQLAlchemyAsyncRepositoryService[Account]):

    class Repo(SQLAlchemyAsyncRepository[Account]):
        model_type = Account

    repository_type = Repo