from enum import Enum
from typing import Annotated
from uuid import UUID
from advanced_alchemy.extensions.litestar import providers, service
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
from app.core.dependencies import (
    create_order_provider,
    create_search_provider,
    provide_filter_list,
    provide_pagination,
)
from app.common.response import COMMON_RESPONSES, ResponseSchema, SuccessResponse
from app.modules.system.user.schema import UserCreate, UserRead, UserUpdate
from app.modules.system.user.service import UserService


# 定义模型字段枚举
class UserSortField(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    DESCRIPTION = "description"
    PHONE = "phone"


class UserController(Controller):
    path = "/users"
    tags = ["User Management"]

    dependencies = {
        **providers.create_service_dependencies(
            UserService,
            "user_service",
        )
    }

    @get(
        "/",
        responses={
            200: ResponseSpec(
                data_container=ResponseSchema[service.OffsetPagination[UserRead]],
                description="用戶列表",
            ),
            **COMMON_RESPONSES,
        },
        dependencies={
            "pagination": Provide(provide_pagination),
            "order": create_order_provider(UserSortField),
            "search_filter": create_search_provider(
                ["username", "description", "phone"]
            ),
            "filters_list": Provide(provide_filter_list),
        },
    )
    async def list_users(
        self,
        user_service: UserService,
        search_filter: Annotated[SearchFilter, Dependency(skip_validation=True)],
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
        order: Annotated[OrderBy, Dependency(skip_validation=True)],
        filters_list: Annotated[list[ComparisonFilter], Dependency(skip_validation=True)],
    ) -> ResponseSchema[service.OffsetPagination[UserRead]]:

        data = await user_service.search_users(
            search_filter, pagination, order, filters_list
        )

        return SuccessResponse(
            data=data,
            detail="用戶列表查詢成功",
        )

    @get(
        "/{user_id:uuid}",
        responses={
            200: ResponseSpec(
                data_container=ResponseSchema[UserRead],
                description="獲取用戶信息",
            ),
            **COMMON_RESPONSES,
        },
    )
    async def get_user(
        self, user_service: UserService, user_id: UUID
    ) -> ResponseSchema[UserRead]:

        result = await user_service.get(user_id)

        return SuccessResponse(
            data=user_service.to_schema(result, schema_type=UserRead),
            detail="用戶查詢成功",
        )

    @post("/", responses={**COMMON_RESPONSES})
    async def create_user(
        self, user_service: UserService, data: UserCreate
    ) -> ResponseSchema[UserRead]:
        result = await user_service.create(data)

        return SuccessResponse(
            data=user_service.to_schema(result, schema_type=UserRead),
            detail="用戶創建成功",
        )

    @patch("/{user_id:uuid}", responses={**COMMON_RESPONSES})
    async def update_user(
        self, user_service: UserService, data: UserUpdate, user_id: UUID
    ) -> ResponseSchema[UserRead]:
        result = await user_service.update(data, item_id=user_id)
        return SuccessResponse(
            data=user_service.to_schema(result, schema_type=UserRead),
            detail="用戶更新成功",
        )

    @delete(
        "/{user_id:uuid}",
        responses={
            **COMMON_RESPONSES,
            200: ResponseSpec(
                data_container=ResponseSchema[UserRead],
                description="操作結果",
            ),
        },
        status_code=200,
    )
    async def delete_user(
        self, user_service: UserService, user_id: UUID
    ) -> ResponseSchema[UserRead]:
        result = await user_service.delete(user_id)
        return SuccessResponse(
            data=user_service.to_schema(result, schema_type=UserRead),
            detail="用戶已刪除",
        )
