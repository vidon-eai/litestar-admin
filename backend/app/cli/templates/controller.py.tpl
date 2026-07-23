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
from {module_import_path}.schema import (
    {pascal_name}Create,
    {pascal_name}Read,
    {pascal_name}Update,
)
from {module_import_path}.service import {pascal_name}Service

class {pascal_name}OrderFields(Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class {pascal_name}Controller(Controller):
    path = "/{kebab_name}s"
    tags = ["{tag_name}"]
    dependencies = {{
        **providers.create_service_dependencies(
            {pascal_name}Service,
            "{snake_name}_service",
        ),
    }}

    @get(
        "/",
        summary="{tag_name}列表",
        responses={{
            **COMMON_RESPONSES,
        }},
        dependencies={{
            "pagination": Provide(provide_pagination),
            "search_filter": Provide(create_search_provider({{"name"}})),
            "order_filter": Provide(
                create_order_provider(
                    order_enum={pascal_name}OrderFields, default_field="created_at"
                )
            ),
        }},
    )
    async def list_{snake_name}s(
        self,
        {snake_name}_service: {pascal_name}Service,
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
        search_filter: Annotated[
            SearchFilter | None, Dependency(skip_validation=True)
        ] = None,
        order_filter: Annotated[
            OrderBy | None, Dependency(skip_validation=True)
        ] = None,
    ) -> ApiResponse[OffsetPagination[{pascal_name}Read]]:

        filters = [pagination]
        if search_filter:
            filters.append(search_filter)

        if order_filter:
            filters.append(order_filter)

        results, total_count = await {snake_name}_service.list_and_count(*filters)

        return ApiResponse(
            data={snake_name}_service.to_schema(
                results, total=total_count, filters=filters, schema_type={pascal_name}Read
            ),
            detail="{tag_name}列表獲取成功",
        )

    @get(
        "/{{{snake_name}_id:uuid}}",
        summary="{tag_name}詳情",
        responses={{
            **COMMON_RESPONSES,
        }},
    )
    async def get_{snake_name}(
        self,
        {snake_name}_service: {pascal_name}Service,
        {snake_name}_id: UUID,
    ) -> ApiResponse[{pascal_name}Read]:
        result = await {snake_name}_service.get({snake_name}_id)

        return ApiResponse(
            data={snake_name}_service.to_schema(result, schema_type={pascal_name}Read),
            detail="{tag_name}詳情獲取成功",
        )

    @post(
        summary="創建{tag_name}",
        responses={{
            **COMMON_RESPONSES,
        }},
    )
    async def create_{snake_name}(
        self,
        {snake_name}_service: {pascal_name}Service,
        data: {pascal_name}Create,
    ) -> ApiResponse[{pascal_name}Read]:
        result = await {snake_name}_service.create(data)

        return ApiResponse(
            data={snake_name}_service.to_schema(result, schema_type={pascal_name}Read),
            detail="{tag_name}創建成功",
        )

    @patch(
        "/{{{snake_name}_id:uuid}}",
        summary="更新{tag_name}",
        responses={{
            **COMMON_RESPONSES,
        }},
    )
    async def update_{snake_name}(
        self,
        {snake_name}_service: {pascal_name}Service,
        {snake_name}_id: UUID,
        data: {pascal_name}Update,
    ) -> ApiResponse[{pascal_name}Read]:
        result = await {snake_name}_service.update(data, {snake_name}_id)

        return ApiResponse(
            data={snake_name}_service.to_schema(result, schema_type={pascal_name}Read),
            detail="{tag_name}更新成功",
        )

    @delete(
        "/{{{snake_name}_id:uuid}}",
        summary="刪除{tag_name}",
        responses={{
            **COMMON_RESPONSES,
        }},
        status_code=HTTP_200_OK,
    )
    async def delete_{snake_name}(
        self,
        {snake_name}_service: {pascal_name}Service,
        {snake_name}_id: UUID,
    ) -> ApiResponse[None]:
        await {snake_name}_service.delete({snake_name}_id)

        return ApiResponse(
            data=None,
            detail="{tag_name}刪除成功",
        )