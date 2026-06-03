from __future__ import annotations
import hashlib
from typing import TYPE_CHECKING
from advanced_alchemy.service import (
    SQLAlchemyAsyncRepositoryService,
    schema_dump,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.db.models.models import Account

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

if TYPE_CHECKING:
    from advanced_alchemy.service import ModelDictT


class AccountService(SQLAlchemyAsyncRepositoryService[Account]):

    class Repo(SQLAlchemyAsyncRepository[Account]):
        model_type = Account

    repository_type = Repo
