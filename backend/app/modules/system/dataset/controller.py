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
    create_search_provider,
    provide_pagination,
)
from app.modules.system.dataset.schema import (
    DatasetCreate,
    DatasetRead,
    DatasetUpdate,
    DatesetWithCollectionsRead,
)
from app.modules.system.dataset.service import DatasetService
from app.modules.system.user.schema import UserRead
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK


class DatasetOrderFields(Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class DatasetController(Controller):
    path = "/datasets"
    tags = ["知識庫管理模塊"]
    dependencies = {
        **providers.create_service_dependencies(
            DatasetService,
            "dataset_service",
        ),
    }

    @get(
        "/",
        summary="知識庫列表",
        responses={
            **COMMON_RESPONSES,
        },
        dependencies={
            "pagination": Provide(provide_pagination),
            "search_filter": Provide(create_search_provider({"name"})),
            "order_filter": Provide(
                create_order_provider(
                    order_enum=DatasetOrderFields, default_field="created_at"
                )
            ),
        },
    )
    async def list_datasets(
        self,
        dataset_service: DatasetService,
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
        search_filter: Annotated[
            SearchFilter | None, Dependency(skip_validation=True)
        ] = None,
        order_filter: Annotated[
            OrderBy | None, Dependency(skip_validation=True)
        ] = None,
    ) -> ApiResponse[OffsetPagination[DatasetRead]]:

        filters = [pagination]
        if search_filter:
            filters.append(search_filter)

        if order_filter:
            filters.append(order_filter)

        results, total_count = await dataset_service.list_and_count(*filters)

        return ApiResponse(
            data=dataset_service.to_schema(
                results, total=total_count, filters=filters, schema_type=DatasetRead
            ),
            detail="知識庫列表獲取成功",
        )

    @get(
        "/{dataset_id:uuid}",
        summary="知識庫詳情",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def get_dataset(
        self,
        dataset_service: DatasetService,
        dataset_id: UUID,
    ) -> ApiResponse[DatasetRead]:
        result = await dataset_service.get(dataset_id)

        return ApiResponse(
            data=dataset_service.to_schema(result, schema_type=DatasetRead),
            detail="知識庫詳情獲取成功",
        )

    @post(
        summary="創建知識庫",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def create_dataset(
        self,
        dataset_service: DatasetService,
        data: DatasetCreate,
        current_user: UserRead = None,
    ) -> ApiResponse[DatasetRead]:
        data.created_by = current_user.id
        result = await dataset_service.create(data)

        return ApiResponse(
            data=dataset_service.to_schema(result, schema_type=DatasetRead),
            detail="知識庫創建成功",
        )

    @patch(
        "/{dataset_id:uuid}",
        summary="更新知識庫",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def update_dataset(
        self, dataset_service: DatasetService, dataset_id: UUID, data: DatasetUpdate
    ) -> ApiResponse[DatasetRead]:
        result = await dataset_service.update(data, dataset_id)

        return ApiResponse(
            data=dataset_service.to_schema(result, schema_type=DatasetRead),
            detail="知識庫更新成功",
        )

    @delete(
        "/{dataset_id:uuid}",
        summary="刪除知識庫",
        responses={
            **COMMON_RESPONSES,
        },
        status_code=HTTP_200_OK,
    )
    async def delete_role(
        self, dataset_service: DatasetService, dataset_id: UUID
    ) -> ApiResponse[None]:
        await dataset_service.delete(dataset_id)

        return ApiResponse(
            data=None,
            detail="知識庫刪除成功",
        )

    @get(
        "/{dataset_id:uuid}/documents",
        summary="知識庫詳情",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def get_documents(
        self,
        dataset_service: DatasetService,
        dataset_id: UUID,
    ) -> ApiResponse[DatesetWithCollectionsRead]:
        result = await dataset_service.get_dataset_with_collections(
            dataset_id=dataset_id
        )

        return ApiResponse(
            data=dataset_service.to_schema(
                result, schema_type=DatesetWithCollectionsRead
            ),
            detail="知識庫詳情獲取成功",
        )
