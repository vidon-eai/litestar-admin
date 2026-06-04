from __future__ import annotations

from typing import Sequence
from advanced_alchemy.service import (
    SQLAlchemyAsyncRepositoryService,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.db.models.models import Tenant



class TenantService(SQLAlchemyAsyncRepositoryService[Tenant]):

    class Repo(SQLAlchemyAsyncRepository[Tenant]):
        model_type = Tenant
        order_by = [Tenant.id.desc()]

    repository_type = Repo

    async def list(self, *args, order_by=None, **kwargs) -> Sequence[Tenant]:
        if order_by is None:
            order_by = self.repository_type.order_by
        return await super().list(*args, order_by=order_by, **kwargs)

    async def list_and_count(
        self, *args, order_by=None, **kwargs
    ) -> tuple[Sequence[Tenant], int]:
        if order_by is None:
            order_by = self.repository_type.order_by
        return await super().list_and_count(*args, order_by=order_by, **kwargs)
