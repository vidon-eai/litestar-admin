from advanced_alchemy.filters import ComparisonFilter, LimitOffset, OrderBy, SearchFilter
from advanced_alchemy.service import (
    OffsetPagination,
    SQLAlchemyAsyncRepositoryService,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.modules.system.user.model import User
from app.modules.system.user.schema import UserRead

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from litestar.repository.filters import LimitOffset


class UserService(SQLAlchemyAsyncRepositoryService[User]):

    class Repo(SQLAlchemyAsyncRepository[User]):
        model_type = User

    repository_type = Repo

    async def search_users(
        self,
        search_filter: SearchFilter,
        pagination: LimitOffset,
        order_by: OrderBy | None,
        filters_list: list[ComparisonFilter] | None = None
    ) -> OffsetPagination[UserRead]:

        filters = [
            pagination
        ]

        if order_by: filters.append(order_by)
        if search_filter: filters.append(search_filter)
            
        if filters_list:
            filters.extend(filters_list)

        results, total = await self.list_and_count(*filters)

        return self.to_schema(results, total, filters=filters, schema_type=UserRead)
