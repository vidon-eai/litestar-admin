from typing import TYPE_CHECKING
from advanced_alchemy.filters import ComparisonFilter, LimitOffset, OrderBy, SearchFilter
from advanced_alchemy.service import (
    OffsetPagination,
    SQLAlchemyAsyncRepositoryService,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.modules.system.post.model import Post

from app.modules.system.post.schema import PostRead


class PostRepo(SQLAlchemyAsyncRepository[Post]):
        model_type = Post

class PostService(SQLAlchemyAsyncRepositoryService[Post]):

    repository_type = PostRepo
    
    async def search_posts(
        self,
        search_filter: SearchFilter,
        pagination: LimitOffset,
        order_by: OrderBy | None,
    ) -> OffsetPagination[PostRead]:

        filters = [
            pagination
        ]

        if order_by: filters.append(order_by)
        if search_filter: filters.append(search_filter)
            
        results, total = await self.list_and_count(*filters)

        return self.to_schema(results, total, filters=filters, schema_type=PostRead)