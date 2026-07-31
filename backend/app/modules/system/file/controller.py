import mimetypes
import os
import uuid
from enum import Enum
from typing import Annotated

from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import FilterTypes, LimitOffset, OrderBy, SearchFilter
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
from app.modules.system.collection.service import CollectionService
from app.modules.system.file.schema import FileRead, UploadFileFormData
from app.modules.system.file.service import FileService
from app.modules.system.user.schema import UserRead
from app.plugins.storage.service import StorageService
from litestar import Controller, Response, delete, get, post
from litestar.di import Provide
from litestar.exceptions import HTTPException, NotFoundException
from litestar.params import Dependency, MultipartBody


class FileOrderFields(Enum):
    created_at = "created_at"
    updated_at = "updated_at"


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8002/api/v1")


class FileController(Controller):
    path = "/files"
    tags = ["文件管理模塊"]
    dependencies = {
        **providers.create_service_dependencies(
            FileService,
            "file_service",
        ),
    }

    @get(
        "/",
        summary="文件列表",
        responses={
            **COMMON_RESPONSES,
        },
        dependencies={
            "pagination": Provide(create_pagination_provider),
            "search_filter": Provide(create_search_provider({"name"})),
            "order_filter": Provide(
                create_order_provider(
                    order_enum=FileOrderFields, default_field="created_at"
                )
            ),
        },
    )
    async def list_files(
        self,
        file_service: FileService,
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
        search_filter: Annotated[
            SearchFilter | None, Dependency(skip_validation=True)
        ] = None,
        order_filter: Annotated[
            OrderBy | None, Dependency(skip_validation=True)
        ] = None,
    ) -> ApiResponse[OffsetPagination[FileRead]]:

        filters: list[FilterTypes] = []
        for filter_item in (pagination, search_filter, order_filter):
            if filter_item:
                filters.append(filter_item)

        results, total_count = await file_service.list_and_count(*filters)

        return ApiResponse(
            data=file_service.to_schema(
                results, total=total_count, filters=filters, schema_type=FileRead
            ),
            detail="文件列表獲取成功",
        )

    @post(
        "/upload",
        summary="上傳文件",
        responses={
            **COMMON_RESPONSES,
        },
        request_max_body_size=100 * 1024 * 1024,  # 100MB
        dependencies={
            **providers.create_service_dependencies(
                CollectionService, "collection_service"
            )
        },
    )
    async def upload_file(
        self,
        storage_service: StorageService,
        file_service: FileService,
        collection_service: CollectionService,
        data: MultipartBody[UploadFileFormData],
        current_user: UserRead,
    ) -> ApiResponse[FileRead]:
        dataset_id = data.dataset_id
        content = await data.file.read()
        filename = data.file.filename
        content_type = data.file.content_type
        extension = os.path.splitext(filename)[1].lstrip(".").lower()
        filesize = len(content)
        file_uuid = uuid.uuid4()
        file_key = (
            str(current_user.id)
            + "/datasets/"
            + str(dataset_id)
            + "/"
            + str(file_uuid)
            + "."
            + extension
        )
        success = await storage_service.put(file_key, content)
        if not success:
            raise HTTPException(status_code=500, detail="文件保存失败")
        file = await file_service.create(
            {
                "created_by": current_user.id,
                "name": filename,
                "location": file_key,
                "size": filesize,
                "type": content_type,
                "storage_type": storage_service.storage_type,
            }
        )

        try:
            await collection_service.create(
                {"file": file, "dataset_id": dataset_id, "name": file.name}
            )
        except Exception as e:
            await storage_service.delete(file_key)
            await file_service.delete(file.id)

            raise HTTPException(status_code=500, detail=str(e))

        return ApiResponse(
            data=file_service.to_schema(file, schema_type=FileRead),
            detail="文件上傳成功",
        )

    @get("/download/{file_id:uuid}")
    async def download_file(
        self,
        file_service: FileService,
        file_id: uuid.UUID,
        storage_service: StorageService,
    ) -> Response[bytes]:
        file = await file_service.get_one_or_none(id=file_id)
        if file is None:
            raise NotFoundException(detail="文件不存在")

        content = await storage_service.get(file.location)
        if not content:
            raise NotFoundException(detail="文件不存在")

        return Response(
            content=content,
            headers={"Content-Disposition": f'attachment; filename="{file.name}"'},
            media_type="application/octet-stream",
        )

    @delete(
        "/{file_id:uuid}",
        summary="刪除文件",
        responses={
            **COMMON_RESPONSES,
        },
        status_code=200,
    )
    async def delete_file(
        self,
        file_service: FileService,
        file_id: uuid.UUID,
        storage_service: StorageService,
    ) -> ApiResponse[None]:

        file = await file_service.get_one_or_none(id=file_id)
        if file is None:
            raise NotFoundException(detail="文件不存在")

        # Delete from storage
        await storage_service.delete(file.location)

        await file_service.delete(file_id)
        return ApiResponse(data=None, detail="文件刪除成功")

    @get(
        "/preview/{file_key:path}",
        summary="預覽圖片/文件",
        description="根據存储 file_key 直接返回文件流或重定向至 S3 預覽链接",
        exclude_from_auth=True,
    )
    async def preview_file(
        self,
        file_key: str,
        storage_service: StorageService,
    ) -> Response[bytes]:
        # 1. 如果是 S3 存储，直接获取预签名 URL 重定向
        if storage_service.storage_type == "s3":
            url = await storage_service.get_url(file_key)
            if not url:
                raise NotFoundException(detail="圖片不存在或無法生成預覽 URL")

        # 2. 如果是本地存储，从存储中读取内容字节流
        content = await storage_service.get(file_key)
        if not content:
            raise NotFoundException(detail="圖片不存在")

        # 动态推断 Content-Type (例如 image/png, image/jpeg)
        media_type, _ = mimetypes.guess_type(file_key)
        if not media_type:
            media_type = "image/png"  # 默认降级格式

        return Response(
            content=content,
            media_type=media_type,
            headers={
                "Content-Disposition": f'inline; filename="{os.path.basename(file_key)}"',
                "Cache-Control": "public, max-age=86400",
                # 显式允许前端跨域加载图片
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
            },
        )
