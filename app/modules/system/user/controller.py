from typing import Annotated
from uuid import UUID
from advanced_alchemy.extensions.litestar import filters, providers, service
from advanced_alchemy.filters import LimitOffset, SearchFilter
from litestar import Controller, delete, get, patch, post
from litestar.openapi.datastructures import ResponseSpec
from litestar.params import Dependency
from litestar.status_codes import HTTP_204_NO_CONTENT
from app.common.response import COMMON_RESPONSES, ResponseSchema, SuccessResponse
from app.modules.system.user.model import UserCreate, UserRead, UserUpdate
from app.modules.system.user.service import UserService
from advanced_alchemy.filters import PaginationFilter


class UserController(Controller):
    path = "/users"
    tags = ["User Management"]

    dependencies = providers.create_service_dependencies(
        UserService,
        "user_service",
        filters={
            "pagination_type": "limit_offset",
            "sort_order": "asc",
            "sort_field": "username",
            # 使用字典格式可以更精確地覆蓋預設行為
            "search": (["username", "description", "email", "phone"], "search"),
            "pagination_size": 10,
        },
    )

    @get(
        "/",
        responses={
            200: ResponseSpec(
                data_container=ResponseSchema[service.OffsetPagination[UserRead]],
                description="用戶列表",
            ),
            **COMMON_RESPONSES,
        },
    )
    async def list_users(
        self,
        user_service: UserService,
        filters: Annotated[list[filters.FilterTypes], Dependency(skip_validation=True)],
    ) -> ResponseSchema[service.OffsetPagination[UserRead]]:

        results, total = await user_service.list_and_count(*filters)
        return SuccessResponse(
            data=user_service.to_schema(
                results, total, filters=filters, schema_type=UserRead
            ),
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
