from enum import Enum
from typing import Annotated
from uuid import UUID

from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.service import OffsetPagination
from app.common.response import COMMON_RESPONSES, ApiResponse
from app.db.models.dataset import Collection
from app.modules.system.data.schema import (
    DataCreate,
    DataRead,
    DataUpdate,
)
from app.modules.system.data.service import DataService
from litestar import Controller, delete, get, patch, post
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK


class DataOrderFields(Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class DataController(Controller):
    path = "/{collection_id:uuid}/datas"
    tags = ["文檔切片數據模塊"]
    dependencies = {
        **providers.create_service_dependencies(
            DataService,
            "data_service",
        ),
    }

    @get(
        "/",
        summary="文檔切片數據模塊列表",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def list_datas(
        self,
        collection_id: UUID,
        data_service: DataService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> ApiResponse[OffsetPagination[DataRead]]:

        results, total_count = await data_service.list_and_count(
            *filters,
            Collection.id == collection_id,
        )

        return ApiResponse(
            data=data_service.to_schema(
                results, total=total_count, filters=filters, schema_type=DataRead
            ),
            detail="文檔切片數據模塊列表獲取成功",
        )

    @get(
        "/{data_id:uuid}",
        summary="文檔切片數據模塊詳情",
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
            detail="文檔切片數據模塊詳情獲取成功",
        )

    @post(
        summary="創建文檔切片數據模塊",
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
            detail="文檔切片數據模塊創建成功",
        )

    @patch(
        "/{data_id:uuid}",
        summary="更新文檔切片數據模塊",
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
            detail="文檔切片數據模塊更新成功",
        )

    @delete(
        "/{data_id:uuid}",
        summary="刪除文檔切片數據模塊",
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
            detail="文檔切片數據模塊刪除成功",
        )
