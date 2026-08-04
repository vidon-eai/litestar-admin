from enum import Enum
from typing import Annotated
from uuid import UUID

from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.service import OffsetPagination
from app.common.response import (
    COMMON_RESPONSES,
    ApiResponse,
)
from app.modules.system.role.schema import RoleCreate, RoleRead, RoleUpdate
from app.modules.system.role.service import RoleService
from litestar import Controller, delete, get, patch, post
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK


class RoleOrderFields(str, Enum):
    NAME = "name"
    CREATED_AT = "created_at"


class RoleController(Controller):
    path = "/roles"
    tags = ["角色管理模塊"]
    dependencies = {
        **providers.create_service_dependencies(
            RoleService,
            "role_service",
        )
    }

    @get(
        "/",
        summary="角色列表",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def list_roles(
        self,
        role_service: RoleService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> ApiResponse[OffsetPagination[RoleRead]]:

        results, total_count = await role_service.list_and_count(*filters)

        return ApiResponse(
            data=role_service.to_schema(
                results, total=total_count, filters=filters, schema_type=RoleRead
            ),
            detail="角色列表獲取成功",
        )

    @get(
        "/{role_id:uuid}",
        summary="角色詳情",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def get_role(
        self,
        role_service: RoleService,
        role_id: UUID,
    ) -> ApiResponse[RoleRead]:
        result = await role_service.get(role_id)

        return ApiResponse(
            data=role_service.to_schema(result, schema_type=RoleRead),
            detail="角色詳情獲取成功",
        )

    @post(
        summary="創建角色",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def create_role(
        self, role_service: RoleService, data: RoleCreate
    ) -> ApiResponse[RoleRead]:
        result = await role_service.create(data)

        return ApiResponse(
            data=role_service.to_schema(result, schema_type=RoleRead),
            detail="角色創建成功",
        )

    @patch(
        "/{role_id:uuid}",
        summary="更新角色",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def update_role(
        self, role_service: RoleService, role_id: UUID, data: RoleUpdate
    ) -> ApiResponse[RoleRead]:
        result = await role_service.update(data, role_id)

        return ApiResponse(
            data=role_service.to_schema(result, schema_type=RoleRead),
            detail="角色更新成功",
        )

    @delete(
        "/{role_id:uuid}",
        summary="刪除角色",
        responses={
            **COMMON_RESPONSES,
        },
        status_code=HTTP_200_OK,
    )
    async def delete_role(
        self, role_service: RoleService, role_id: UUID
    ) -> ApiResponse[None]:
        await role_service.delete(role_id)

        return ApiResponse(
            data=None,
            detail="角色刪除成功",
        )
