from enum import Enum
from typing import Annotated
from uuid import UUID

from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import LimitOffset, OrderBy, SearchFilter
from advanced_alchemy.service import OffsetPagination
from app.common.response import (
    COMMON_RESPONSES,
    ApiResponse,
)
from app.core.dependencies import (
    create_order_provider,
    create_pagination_provider,
    create_search_provider,
)
from app.modules.system.user.schema import UserCreate, UserRead, UserUpdate
from app.modules.system.user.service import UserService
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK


class UserOrderFields(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    CREATED_AT = "created_at"


class UserController(Controller):
    path = "/users"
    tags = ["用戶管理模塊"]
    dependencies = {
        **providers.create_service_dependencies(
            UserService,
            "user_service",
        )
    }

    @get(
        "/",
        summary="用戶列表",
        responses={
            **COMMON_RESPONSES,
        },
        dependencies={
            "pagination": Provide(create_pagination_provider),
            "search_filter": Provide(create_search_provider({"username", "email"})),
            "order_filter": Provide(
                create_order_provider(
                    order_enum=UserOrderFields, default_field="created_at"
                )
            ),
        },
    )
    async def list_users(
        self,
        user_service: UserService,
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
        search_filter: Annotated[
            SearchFilter | None, Dependency(skip_validation=True)
        ] = None,
        order_filter: Annotated[
            OrderBy | None, Dependency(skip_validation=True)
        ] = None,
    ) -> ApiResponse[OffsetPagination[UserRead]]:

        filters = [pagination]
        if search_filter:
            filters.append(search_filter)

        if order_filter:
            filters.append(order_filter)

        results, total_count = await user_service.list_and_count(*filters)

        return ApiResponse(
            data=user_service.to_schema(
                results, total=total_count, filters=filters, schema_type=UserRead
            ),
            detail="用戶列表獲取成功",
        )

    @get(
        "/{user_id:uuid}",
        summary="用戶詳情",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def get_user(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> ApiResponse[UserRead]:
        result = await user_service.get(user_id)

        return ApiResponse(
            data=user_service.to_schema(result, schema_type=UserRead),
            detail="用戶詳情獲取成功",
        )

    @post(
        summary="創建用戶",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def create_user(
        self, user_service: UserService, data: UserCreate, current_user: UserRead
    ) -> ApiResponse[UserRead]:
        data.created_by = current_user.id
        result = await user_service.create(data)

        return ApiResponse(
            data=user_service.to_schema(result, schema_type=UserRead),
            detail="用戶創建成功",
        )

    @patch(
        "/{user_id:uuid}",
        summary="更新用戶",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def update_user(
        self,
        user_service: UserService,
        user_id: UUID,
        data: UserUpdate,
        current_user: UserRead,
    ) -> ApiResponse[UserRead]:
        data.updated_by = current_user.id
        result = await user_service.update(data, user_id)

        return ApiResponse(
            data=user_service.to_schema(result, schema_type=UserRead),
            detail="用戶更新成功",
        )

    @delete(
        "/{user_id:uuid}",
        summary="刪除用戶",
        responses={
            **COMMON_RESPONSES,
        },
        status_code=HTTP_200_OK,
    )
    async def delete_user(
        self, user_service: UserService, user_id: UUID
    ) -> ApiResponse[None]:
        await user_service.delete(user_id)

        return ApiResponse(
            data=None,
            detail="用戶刪除成功",
        )

    @post(
        "/{user_id:uuid}/roles",
        summary="分配用戶角色",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def assign_roles_to_user(
        self,
        user_service: UserService,
        user_id: UUID,
        role_ids: list[UUID] | None = None,
    ) -> ApiResponse[UserRead]:
        user = await user_service.get(user_id)
        user.role_ids = role_ids or []

        await user_service.update(user)

        return ApiResponse(
            data=user_service.to_schema(user, schema_type=UserRead),
            detail="用戶角色分配成功",
        )
