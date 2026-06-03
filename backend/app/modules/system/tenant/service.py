from __future__ import annotations

from typing import TYPE_CHECKING, Sequence
from uuid import UUID
from advanced_alchemy.service import (
    SQLAlchemyAsyncRepositoryService,
    schema_dump,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.db.models.models import AccountTenantAssociation, Tenant

if TYPE_CHECKING:
    from advanced_alchemy.service import ModelDictT


class TenantService(SQLAlchemyAsyncRepositoryService[Tenant]):

    class Repo(SQLAlchemyAsyncRepository[Tenant]):
        model_type = Tenant
        order_by = [Tenant.id.desc()]

    repository_type = Repo

    async def update(self, data: ModelDictT[Tenant], item_id: UUID, **kwargs):
        data = schema_dump(data)
        accounts_data = data.pop("accounts", None)

        tenant = await self.get(item_id=item_id)

        for key, value in data.items():
            if hasattr(tenant, key) and key != "accounts":
                setattr(tenant, key, value)

        if accounts_data is not None:
            existing_associations = {
                assoc.account_id: assoc for assoc in tenant.accounts
            }

            new_accounts_ids = set()

            for acc_data in accounts_data:
                acc_id = (
                    acc_data["account_id"]
                    if isinstance(acc_data, dict)
                    else acc_data.account_id
                )
                role = acc_data["role"] if isinstance(acc_data, dict) else acc_data.role
                new_accounts_ids.add(acc_id)

                if acc_id in existing_associations:
                    existing_associations[acc_id].role = role
                else:
                    new_assoc = AccountTenantAssociation(
                        tenant_id=tenant.id, account_id=acc_id, role=role
                    )
                    tenant.accounts.append(new_assoc)

            for acc_id, assoc in list(existing_associations.items()):
                if acc_id not in new_accounts_ids:
                    tenant.accounts.remove(assoc)

        return await super().update(data=tenant, item_id=item_id, **kwargs)

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

    async def _populate_with_accounts(self, tenant: Tenant) -> Tenant:
        """Populate tenant with account information"""
        # This would need to be implemented based on your specific requirements
        # For now, we'll just return the tenant as-is
        return tenant
