from email.policy import HTTP
from turtle import pos
from typing import Annotated, Generic, TypeVar
from uuid import UUID
from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import LimitOffset
from advanced_alchemy.service import OffsetPagination
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK
from app.core.dependencies import (
    provide_pagination,
)
from app.common.response import (
    COMMON_RESPONSES,
    ApiResponse,
)
from app.modules.system.tenant.service import TenantService
from app.modules.system.tenant.schema import TenantRead, TenantCreate, TenantUpdate


class TenantController(Controller):
    path = "/tenants"
    tags = ["租戶管理模塊"]
    dependencies = {
        **providers.create_service_dependencies(
            TenantService,
            "tenant_service",
        )
    }

    @get(
        "/",
        summary="租戶列表",
        responses={
            **COMMON_RESPONSES,
        },
        dependencies={
            "pagination": Provide(provide_pagination),
        },
    )
    async def list_tenants(
        self,
        tenant_service: TenantService,
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
    ) -> ApiResponse[OffsetPagination[TenantRead]]:

        filters = [pagination]

        results, total_count = await tenant_service.list_and_count(*filters)

        return ApiResponse(
            data=tenant_service.to_schema(
                results,
                total=total_count,
                filters=filters,
                schema_type=TenantRead,
            ),
            detail="租戶列表獲取成功",
        )

    @get(
        "/{tenant_id:uuid}",
        responses={
            **COMMON_RESPONSES,
        },
        summary="獲取租戶",
    )
    async def get_tenant(
        self,
        tenant_service: TenantService,
        tenant_id: UUID,
    ) -> ApiResponse[TenantRead]:
        try:
            result = await tenant_service.get(tenant_id)
        except Exception:
            raise NotFoundError("租戶不存在")

        return ApiResponse(
            data=tenant_service.to_schema(result, schema_type=TenantRead),
            detail="租戶獲取成功",
        )

    @post(
        "/",
        summary="創建租戶",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def create_tenant(
        self,
        tenant_service: TenantService,
        data: TenantCreate,
    ) -> ApiResponse[TenantRead]:
        result = await tenant_service.create(data)

        return ApiResponse(
            data=tenant_service.to_schema(result, schema_type=TenantRead),
            detail="租戶創建成功",
        )

    @patch(
        "/{tenant_id:uuid}",
        responses={
            **COMMON_RESPONSES,
        },
        summary="更新租戶",
    )
    async def update_tenant(
        self,
        tenant_service: TenantService,
        tenant_id: UUID,
        data: TenantUpdate,
    ) -> ApiResponse[TenantRead]:
        result = await tenant_service.update(data, item_id=tenant_id)
        return ApiResponse(
            data=tenant_service.to_schema(result, schema_type=TenantRead),
            detail="租戶更新成功",
        )

    @delete(
        "/{tenant_id:uuid}",
        responses={
            **COMMON_RESPONSES,
        },
        status_code=HTTP_200_OK,
        summary="刪除租戶",
    )
    async def delete_tenant(
        self,
        tenant_service: TenantService,
        tenant_id: UUID,
    ) -> ApiResponse[TenantRead]:
        result = await tenant_service.delete(tenant_id)
        return ApiResponse(
            data=tenant_service.to_schema(result, schema_type=TenantRead),
            detail="租戶刪除成功",
        )
