import asyncio
import os
import uuid
from typing import Annotated, Any
from uuid import UUID

from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import (
    FilterTypes,
)
from advanced_alchemy.service import OffsetPagination
from app.common.response import (
    COMMON_RESPONSES,
    ApiResponse,
)
from app.modules.system.collection.service import CollectionService
from app.modules.system.data.service import DataService
from app.modules.system.dataset.schema import (
    DatasetCreate,
    DatasetRead,
    DatasetUpdate,
    DatasetWithCollectionsRead,
)
from app.modules.system.dataset.service import DatasetService
from app.modules.system.user.schema import UserRead
from app.plugins.rag.service import RAGService
from app.plugins.storage.service import StorageService
from app.utils.parser.docling_parser import DoclingParser
from litestar import Controller, delete, get, patch, post
from litestar.exceptions import HTTPException, NotFoundException
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK
from pydantic import BaseModel, Field

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8002/api/v1")


class ChatRequest(BaseModel):
    question: str = Field(
        ..., description="使用者提問內容", examples=["什麼是 RAG 技術？"]
    )
    collection: str = Field(
        ..., description="使用者提問內容", examples=["什麼是 RAG 技術？"]
    )
    llm: str = Field(..., description="使用者提問內容", examples=["什麼是 RAG 技術？"])


class DatasetController(Controller):
    path = "/datasets"
    tags = ["知識庫管理模塊"]
    dependencies = {
        **providers.create_service_dependencies(DatasetService, "dataset_service"),
    }

    @get(
        "/",
        summary="知識庫列表",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def list_datasets(
        self,
        dataset_service: DatasetService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> ApiResponse[OffsetPagination[DatasetRead]]:

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
        current_user: UserRead,
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
    async def delete_dataset(
        self, dataset_service: DatasetService, dataset_id: UUID
    ) -> ApiResponse[None]:
        await dataset_service.delete(dataset_id)

        return ApiResponse(
            data=None,
            detail="知識庫刪除成功",
        )

    @get(
        "/{dataset_id:uuid}/documents",
        summary="知識庫文檔列表(含分組)",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def get_documents(
        self,
        dataset_service: DatasetService,
        dataset_id: UUID,
    ) -> ApiResponse[DatasetWithCollectionsRead]:
        result = await dataset_service.get_dataset_with_collections(
            dataset_id=dataset_id
        )

        return ApiResponse(
            data=dataset_service.to_schema(
                result, schema_type=DatasetWithCollectionsRead
            ),
            detail="知識庫文檔列表(含分組)獲取成功",
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
        collection_id: UUID,
        collection_service: CollectionService,
        data_service: DataService,
        dataset_service: DatasetService,
        storage_service: StorageService,
        rag_service: RAGService,
        current_user: UserRead,
    ) -> ApiResponse[list[Any]]:

        collection = await collection_service.get_one(id=collection_id)

        file = collection.file
        if file is None:
            raise NotFoundException(detail="文件不存在")
        if file.storage_type == "local":
            url = url = os.path.join("./storage", file.location)
        elif file.storage_type == "s3":
            url = await storage_service.get_url(file.location)
        else:
            raise ValueError("not support storage type")

        if not url:
            raise HTTPException(status_code=500, detail="生成文件 URL 失敗")

        semaphore = asyncio.Semaphore(5)

        async def handle_image_upload(content: bytes, extension: str) -> str | None:
            async with semaphore:
                try:
                    file_uuid = uuid.uuid4()
                    if not current_user:
                        raise NotFoundException(detail="用戶不存在")
                    user_id = current_user.id
                    file_key = f"{user_id}/datasets/{collection.dataset_id}/{file.id}/images/{file_uuid}.{extension}"

                    success = await storage_service.put(file_key, content)
                    if not success:
                        raise HTTPException(status_code=500, detail="圖片上傳失敗")

                    # 替换为前端可以直接访问的图片预览接口路由路径
                    return f"{API_BASE_URL}/files/preview/{file_key}"
                except Exception:
                    return None

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
        dataset = await dataset_service.get_one(id=collection.dataset_id)
        await rag_service.embed(dataset.name, splits)

        return ApiResponse(
            data=data,
            detail="文檔切片導入知識庫成功",
        )

    @post(
        "/chat",
    )
    async def chat(
        self, rag_service: RAGService, data: ChatRequest
    ) -> ApiResponse[str]:
        result = await rag_service.chat(data.question, data.collection, data.llm)
        return ApiResponse(
            data=result,
            detail="問答成功",
        )
