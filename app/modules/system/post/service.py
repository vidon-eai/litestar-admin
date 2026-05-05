from advanced_alchemy.filters import ComparisonFilter, LimitOffset, OrderBy, SearchFilter
from advanced_alchemy.service import (
    OffsetPagination,
    SQLAlchemyAsyncRepositoryService,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.modules.system.post.model import Post


class PostRepo(SQLAlchemyAsyncRepository[Post]):
        model_type = Post

class PostService(SQLAlchemyAsyncRepositoryService[Post]):

    repository_type = PostRepo