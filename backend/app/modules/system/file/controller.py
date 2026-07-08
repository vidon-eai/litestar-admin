import os
import uuid
from enum import Enum
from typing import Annotated

from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import LimitOffset, OrderBy, SearchFilter
from advanced_alchemy.service import OffsetPagination
from app.common.response import (
    COMMON_RESPONSES,
    ApiResponse,
)
from app.config.setting import app_setting
from app.core.dependencies import (
    create_order_provider,
    create_search_provider,
    provide_pagination,
)
from app.modules.system.file.schema import FileRead
from app.modules.system.file.service import FileService
from app.modules.system.user.schema import UserRead
from app.plugins.storage.service import StorageService
from litestar import Controller, delete, get, post
from litestar.datastructures import UploadFile
from litestar.di import Provide
from litestar.exceptions import HTTPException, NotFoundException
from litestar.params import Dependency, MultipartBody
from litestar.response import File


class FileOrderFields(Enum):
    created_at = "created_at"
    updated_at = "updated_at"





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
            "pagination": Provide(provide_pagination),
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

        filters = [pagination]
        if search_filter:
            filters.append(search_filter)

        if order_filter:
            filters.append(order_filter)

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
    )
    async def upload_file(
        self,
        file_service: FileService,
        data: MultipartBody[UploadFile],
        storage_service: StorageService,
        current_user:UserRead = None,
    ) -> ApiResponse[FileRead]:
        content = data.file.read()
        filename = data.filename
        extension = os.path.splitext(filename)[1].lstrip(".").lower()
        filesize = len(content)
        file_uuid = uuid.uuid4()
        file_key = "uploads" + "/" + str(file_uuid) + "." + extension
        success = await storage_service.put(file_key, content)
        if not success:
            raise HTTPException(status_code=500, detail="文件保存失败")
        file = await file_service.create({
               "created_by": current_user.id,
                "name": data.filename,
                "location": file_key,
                "size": filesize,
                "type": data.content_type,
                "source_type": "LOCAL",
        })

        return ApiResponse(data=file_service.to_schema(file, schema_type=FileRead), detail="文件上傳成功")
      

    @get("/download/{file_id:uuid}")
    async def download_file(
        self,
        file_service: FileService,
        file_id: uuid.UUID,
        storage_service: StorageService,
    ) -> File:
        file = await file_service.get_one_or_none(id=file_id)
        if file is None:
            raise NotFoundException(detail="文件不存在")
        
        content = await storage_service.get(file.location)
        if not content:
            raise NotFoundException(detail="文件不存在")
        
        return File(
            path=app_setting.STORAGE_LOCAL_PATH+"/"+file.location,
            filename=file.name,
            media_type=file.type,
        )

    @delete(
        "/{file_id:uuid}",
        summary="刪除文件",
        responses={
            **COMMON_RESPONSES,
        },
        status_code=200
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
        return ApiResponse(data=None,detail="文件刪除成功")
