from enum import Enum
from typing import Annotated
from uuid import UUID
from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import LimitOffset, OrderBy, SearchFilter
from advanced_alchemy.service import OffsetPagination
from litestar import Controller, get, post
from litestar.di import Provide
from litestar.params import Dependency
from app.core.dependencies import (
    create_order_provider,
    create_search_provider,
    provide_pagination,
)
from app.common.response import (
    COMMON_RESPONSES,
    ApiResponse,
)
from app.modules.system.account.service import AccountService
from app.modules.system.account.schema import AccountCreate, AccountRead


class AccountOrderFields(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    CREATED_AT = "created_at"


class AccountController(Controller):
    path = "/accounts"
    tags = ["賬戶管理模塊"]
    dependencies = {
        **providers.create_service_dependencies(
            AccountService,
            "account_service",
        )
    }

    @get(
        "/",
        summary="賬戶列表",
        responses={
            **COMMON_RESPONSES,
        },
        dependencies={
            "pagination": Provide(provide_pagination),
            "search_filter": Provide(create_search_provider({"username", "email"})),
            "order_filter": Provide(
                create_order_provider(
                    order_enum=AccountOrderFields, default_field="created_at"
                )
            ),
        },
    )
    async def list_accounts(
        self,
        account_service: AccountService,
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
        search_filter: Annotated[
            SearchFilter | None, Dependency(skip_validation=True)
        ] = None,
        order_filter: Annotated[
            OrderBy | None, Dependency(skip_validation=True)
        ] = None,
    ) -> ApiResponse[OffsetPagination[AccountRead]]:

        filters = [pagination]
        if search_filter:
            filters.append(search_filter)

        if order_filter:
            filters.append(order_filter)

        results, total_count = await account_service.list_and_count(*filters)

        return ApiResponse(
            data=account_service.to_schema(
                results, total=total_count, filters=filters, schema_type=AccountRead
            ),
            detail="賬戶列表獲取成功",
        )

    @get(
        "/{account_id:uuid}",
        summary="賬戶詳情",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def get_account(
        self,
        account_service: AccountService,
        account_id: UUID,
    ) -> ApiResponse[AccountRead]:
        result = await account_service.get(account_id)

        return ApiResponse(
            data=account_service.to_schema(result, schema_type=AccountRead),
            detail="賬戶詳情獲取成功",
        )

    @post(
        summary="創建賬戶",
        responses={
            **COMMON_RESPONSES,
        },
    )
    async def create_account(
        self, account_service: AccountService, data: AccountCreate
    ) -> ApiResponse[AccountRead]:
        result = await account_service.create(data)

        return ApiResponse(
            data=account_service.to_schema(result, schema_type=AccountRead),
            detail="賬戶創建成功",
        )
