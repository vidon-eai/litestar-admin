import os
import urllib.parse
import uuid
from enum import Enum
from pathlib import Path
from typing import Annotated

from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import FilterTypes
from advanced_alchemy.service import OffsetPagination
from app.common.response import (
    COMMON_RESPONSES,
    ApiResponse,
)
from app.modules.system.collection.service import CollectionService
from app.modules.system.file.schema import FileRead, UploadFileFormData
from app.modules.system.file.service import FileService
from app.modules.system.user.schema import UserRead
from app.plugins.storage.service import StorageService
from litestar import Controller, Response, delete, get, post
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
    )
    async def list_files(
        self,
        file_service: FileService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> ApiResponse[OffsetPagination[FileRead]]:

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
        raw_filename = data.file.filename
        content_type = data.file.content_type

        file_path = Path(raw_filename)
        extension = file_path.suffix.lstrip(".").lower()
        filename = file_path.stem  # 纯文件名（不含扩展名）
        filesize = len(content)
        file_uuid = uuid.uuid4()
        file_key = (
            str(current_user.id)
            + "/datasets/"
            + str(dataset_id)
            + "/"
            + filename
            + "_"
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
                "name": raw_filename,
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

        encoded_filename = urllib.parse.quote(file.name)

        return Response(
            content=content,
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            },
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
