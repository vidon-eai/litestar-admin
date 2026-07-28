import asyncio
import os
import uuid
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
from app.modules.system.collection.schema import CollectionWithFileRead
from app.modules.system.collection.service import CollectionService
from app.modules.system.data.service import DataService
from app.modules.system.dataset.schema import (
    DatasetCreate,
    DatasetRead,
    DatasetUpdate,
    DatesetWithCollectionsRead,
)
from app.modules.system.dataset.service import DatasetService
from app.modules.system.user.schema import UserRead
from app.plugins.storage.service import StorageService
from app.utils.parser.docling_parser import DoclingParser
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.exceptions import HTTPException, NotFoundException
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8002/api/v1")


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

    @post(
        "/ingest/{collection_id:uuid}",
        dependencies={
            **providers.create_service_dependencies(
                CollectionService, "collection_service"
            ),
            **providers.create_service_dependencies(DataService, "data_service"),
        },
    )
    async def ingest(
        self,
        collection_id: uuid.UUID,
        collection_service: CollectionService,
        data_service: DataService,
        storage_service: StorageService,
        current_user: UserRead = None,
    ) -> ApiResponse[dict[str, str | list]]:

        result = await collection_service.get_one(id=collection_id)
        collection = collection_service.to_schema(
            result, schema_type=CollectionWithFileRead
        )

        file = collection.file
        if file is None:
            raise NotFoundException(detail="文件不存在")
        if file.storage_type == "local":
            url = f"./storage/{file.location}"
        elif file.storage_type == "s3":
            url = await storage_service.get_url(file.location)
        else:
            raise ValueError("not support storage type")

        if not url:
            raise HTTPException(status_code=500, detail="生成文件 URL 失敗")

        semaphore = asyncio.Semaphore(5)

        async def handle_image_upload(content: bytes, extension: str) -> str:
            async with semaphore:
                file_uuid = uuid.uuid4()
                if not current_user:
                    raise NotFoundException(detail="用戶不存在")
                user_id = current_user.id
                file_key = (
                    f"{user_id}/datasets/{file.id}/images/{file_uuid}.{extension}"
                )

                success = await storage_service.put(file_key, content)
                if not success:
                    raise HTTPException(status_code=500, detail="圖片上傳失敗")

                # 替换为前端可以直接访问的图片预览接口路由路径
                return f"{API_BASE_URL}/files/preview/{file_key}"

        parser = DoclingParser(file_path=url)

        documents = list(parser.load_documents())

        await storage_service.delete_dir(f"{current_user.id}/datasets/{file.id}/images")
        await parser.extract_images(documents, upload_fn=handle_image_upload)
        splits = parser.parse(
            documents,
            extra_metadata={
                "filename": file.name,
                "source": file.location,
            },
        )

        data = []
        for split in splits:
            data.append(
                {
                    "dataset_id": collection.dataset_id,
                    "collection_id": collection.id,
                    "question": split.page_content,
                }
            )
        await data_service.delete_where(collection_id=collection.id)
        await data_service.create_many(data)

        return ApiResponse(
            data=data,
            detail="文件 URL 獲取成功",
        )
