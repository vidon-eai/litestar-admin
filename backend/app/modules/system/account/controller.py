from typing import Annotated
from uuid import UUID
from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import LimitOffset
from advanced_alchemy.service import OffsetPagination
from litestar import Controller, get, post
from litestar.di import Provide
from litestar.params import Dependency
from app.core.dependencies import (
    provide_pagination,
)
from app.common.response import (
    COMMON_RESPONSES,
    ApiResponse,
)
from app.modules.system.account.service import AccountService
from app.modules.system.account.schema import AccountCreate, AccountRead


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
        },
    )
    async def list_accounts(
        self,
        account_service: AccountService,
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
    ) -> ApiResponse[OffsetPagination[AccountRead]]:

        filters = [pagination]

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
