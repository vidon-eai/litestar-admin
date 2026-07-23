from enum import Enum
from typing import Annotated
from uuid import UUID

from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import LimitOffset, OrderBy, SearchFilter
from advanced_alchemy.service import OffsetPagination
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK

from app.common.response import ApiResponse, COMMON_RESPONSES
from app.core.dependencies import (
    create_order_provider,
    create_search_provider,
    provide_pagination,
)
from app.modules.system.data.schema import (
    DataCreate,
    DataRead,
    DataUpdate,
)
from app.modules.system.data.service import DataService

class DataOrderFields(Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class DataController(Controller):
    path = "/datas"
    tags = ["Data模塊"]
    dependencies = {
        **providers.create_service_dependencies(
            DataService,
            "data_service",
        ),
    }

    @get(
        "/",
        summary="Data模塊列表",
        responses={
            **COMMON_RESPONSES,
        },
        dependencies={
            "pagination": Provide(provide_pagination),
            "search_filter": Provide(create_search_provider({"name"})),
            "order_filter": Provide(
                create_order_provider(
                    order_enum=DataOrderFields, default_field="created_at"
                )
            ),
        },
    )
    async def list_datas(
        self,
        data_service: DataService,
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
        search_filter: Annotated[
            SearchFilter | None, Dependency(skip_validation=True)
        ] = None,
        order_filter: Annotated[
            OrderBy | None, Dependency(skip_validation=True)
        ] = None,
    ) -> ApiResponse[OffsetPagination[DataRead]]:

        filters = [pagination]
        if search_filter:
            filters.append(search_filter)

        if order_filter:
            filters.append(order_filter)

        results, total_count = await data_service.list_and_count(*filters)

        return ApiResponse(
            data=data_service.to_schema(
                results, total=total_count, filters=filters, schema_type=DataRead
            ),
            detail="Data模塊列表獲取成功",
        )

    @get(
        "/{data_id:uuid}",
        summary="Data模塊詳情",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def get_data(
        self,
        data_service: DataService,
        data_id: UUID,
    ) -> ApiResponse[DataRead]:
        result = await data_service.get(data_id)

        return ApiResponse(
            data=data_service.to_schema(result, schema_type=DataRead),
            detail="Data模塊詳情獲取成功",
        )

    @post(
        summary="創建Data模塊",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def create_data(
        self,
        data_service: DataService,
        data: DataCreate,
    ) -> ApiResponse[DataRead]:
        result = await data_service.create(data)

        return ApiResponse(
            data=data_service.to_schema(result, schema_type=DataRead),
            detail="Data模塊創建成功",
        )

    @patch(
        "/{data_id:uuid}",
        summary="更新Data模塊",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def update_data(
        self,
        data_service: DataService,
        data_id: UUID,
        data: DataUpdate,
    ) -> ApiResponse[DataRead]:
        result = await data_service.update(data, data_id)

        return ApiResponse(
            data=data_service.to_schema(result, schema_type=DataRead),
            detail="Data模塊更新成功",
        )

    @delete(
        "/{data_id:uuid}",
        summary="刪除Data模塊",
        responses={
            **COMMON_RESPONSES,
        },
        status_code=HTTP_200_OK,
    )
    async def delete_data(
        self,
        data_service: DataService,
        data_id: UUID,
    ) -> ApiResponse[None]:
        await data_service.delete(data_id)

        return ApiResponse(
            data=None,
            detail="Data模塊刪除成功",
        )
