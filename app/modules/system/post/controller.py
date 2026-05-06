from enum import Enum
from typing import Annotated
from uuid import UUID
from advanced_alchemy import service
from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import (
    ComparisonFilter,
    LimitOffset,
    OrderBy,
    SearchFilter,
)
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.openapi.datastructures import ResponseSpec
from litestar.params import Dependency
from app.common.response import COMMON_RESPONSES, ResponseSchema, SuccessResponse
from app.core.dependencies import (
    create_order_provider,
    create_search_provider,
    provide_pagination,
)
from app.modules.system.post.schema import PostCreate, PostRead, PostUpdate
from app.modules.system.post.service import PostService


# 定义模型字段枚举
class PostSortField(str, Enum):
    TITLE = "title"
    CONTENT = "content"


class PostController(Controller):
    path = "/posts"
    tags = ["Post Management"]

    dependencies = {
        **providers.create_service_dependencies(
            PostService,
            "post_service",
        )
    }

    @get(
        "/",
        responses={
            200: ResponseSpec(
                data_container=ResponseSchema[service.OffsetPagination[PostRead]],
                description="文章列表",
            ),
            **COMMON_RESPONSES,
        },
        dependencies={
            "pagination": Provide(provide_pagination),
            "order": create_order_provider(PostSortField),
            "search_filter": create_search_provider(["title", "content"]),
        },
    )
    async def list_posts(
        self,
        post_service: PostService,
        search_filter: Annotated[SearchFilter, Dependency(skip_validation=True)],
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
        order: Annotated[OrderBy, Dependency(skip_validation=True)],
    ) -> ResponseSchema[service.OffsetPagination[PostRead]]:

        data = await post_service.search_posts(search_filter, pagination, order)

        return SuccessResponse(
            data=data,
            detail="用戶列表查詢成功",
        )

    @get(
        "/{post_id:uuid}",
        responses={
            200: ResponseSpec(
                data_container=ResponseSchema[PostRead],
                description="獲取文章信息",
            ),
            **COMMON_RESPONSES,
        },
    )
    async def get_post(
        self, post_service: PostService, post_id: UUID
    ) -> ResponseSchema[PostRead]:

        result = await post_service.get(post_id)

        return SuccessResponse(
            data=post_service.to_schema(result, schema_type=PostRead),
            detail="文章查詢成功",
        )

    @post("/", responses={**COMMON_RESPONSES})
    async def create_post(
        self, post_service: PostService, data: PostCreate
    ) -> ResponseSchema[PostRead]:
        result = await post_service.create(data)

        return SuccessResponse(
            data=post_service.to_schema(result, schema_type=PostRead),
            detail="Post創建成功",
        )
        
    @patch("/{post_id:uuid}", responses={**COMMON_RESPONSES})
    async def update_post(
        self, post_service: PostService, data: PostUpdate, post_id:UUID
    ) -> ResponseSchema[PostRead]:
        result = await post_service.update(data, item_id=post_id)
        return SuccessResponse(
            data=post_service.to_schema(result, schema_type=PostRead),
            detail="文章更新成功",
        )
        
    @delete(
        "/{post_id:uuid}",
        responses={
            **COMMON_RESPONSES,
            200: ResponseSpec(
                data_container=ResponseSchema[PostRead],
                description="操作結果",
            ),
        },
        status_code=200,
    )
    async def delete_post(
        self, post_service: PostService, post_id: UUID
    ) -> ResponseSchema[PostRead]:
        result = await post_service.delete(post_id)
        return SuccessResponse(
            data=post_service.to_schema(result, schema_type=PostRead),
            detail="文章已刪除",
        )
