from enum import Enum
from typing import Annotated
from uuid import UUID

from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.service import OffsetPagination
from app.common.response import COMMON_RESPONSES, ApiResponse
from app.db.models.dataset import Collection
from app.modules.system.collection.schema import (
    CollectionCreate,
    CollectionRead,
    CollectionUpdate,
    CollectionWithDatas,
)
from app.modules.system.collection.service import CollectionService
from litestar import Controller, delete, get, patch, post
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK


class CollectionOrderFields(Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class CollectionController(Controller):
    path = "/{dataset_id:uuid}/collections"
    tags = ["知識庫文檔模塊"]
    dependencies = {
        **providers.create_service_dependencies(
            CollectionService,
            "collection_service",
        ),
    }

    @get(
        "/",
        summary="知識庫文檔列表",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def list_collections(
        self,
        dataset_id: UUID,
        collection_service: CollectionService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> ApiResponse[OffsetPagination[CollectionRead]]:

        results, total_count = await collection_service.list_and_count(
            *filters, Collection.dataset_id == dataset_id
        )

        return ApiResponse(
            data=collection_service.to_schema(
                results, total=total_count, filters=filters, schema_type=CollectionRead
            ),
            detail="列表獲取成功",
        )

    @get(
        "/{collection_id:uuid}",
        summary="知識庫文檔詳情",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def get_collection(
        self,
        collection_service: CollectionService,
        collection_id: UUID,
    ) -> ApiResponse[CollectionWithDatas]:
        result = await collection_service.get(collection_id)

        return ApiResponse(
            data=collection_service.to_schema(result, schema_type=CollectionWithDatas),
            detail="詳情獲取成功",
        )

    @post(
        summary="創建文檔",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def create_collection(
        self,
        collection_service: CollectionService,
        data: CollectionCreate,
    ) -> ApiResponse[CollectionRead]:
        result = await collection_service.create(data)

        return ApiResponse(
            data=collection_service.to_schema(result, schema_type=CollectionRead),
            detail="文檔創建成功",
        )

    @patch(
        "/{collection_id:uuid}",
        summary="更新文檔",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def update_collection(
        self,
        collection_service: CollectionService,
        collection_id: UUID,
        data: CollectionUpdate,
    ) -> ApiResponse[CollectionRead]:
        result = await collection_service.update(data, collection_id)

        return ApiResponse(
            data=collection_service.to_schema(result, schema_type=CollectionRead),
            detail="文檔更新成功",
        )

    @delete(
        "/{collection_id:uuid}",
        summary="刪除文檔",
        responses={
            **COMMON_RESPONSES,
        },
        status_code=HTTP_200_OK,
    )
    async def delete_collection(
        self,
        collection_service: CollectionService,
        collection_id: UUID,
    ) -> ApiResponse[None]:
        await collection_service.delete(collection_id)

        return ApiResponse(
            data=None,
            detail="文檔刪除成功",
        )
