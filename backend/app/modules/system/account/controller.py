from email.policy import HTTP
from typing import Annotated, Generic, TypeVar
from uuid import UUID
from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy.filters import LimitOffset
from advanced_alchemy.service import OffsetPagination
from litestar import Controller, MediaType, Response, get
from litestar.di import Provide
from litestar.openapi import ResponseSpec
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK
from pydantic import BaseModel
from app.core.dependencies import (
    provide_pagination,
)
from app.common.response import (
    COMMON_RESPONSES,
    ApiResponse,
    PaginationResponse,
    ResponseSchema,
    SuccessResponse,
)
from app.modules.system.account.service import AccountService
from app.modules.system.account.schema import AccountDTO, AccountRead
from app.db.models.models import Account


T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    status: str = "success"
    code: int = 200
    message: str = "Operation successful"
    data: T  # 這裡會動態填入 DTO 轉換後的資料

    model_config = {"arbitrary_types_allowed": True}


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
        dto=AccountDTO,
    )
    async def list_accounts(
        self,
        account_service: AccountService,
        pagination: Annotated[LimitOffset, Dependency(skip_validation=True)],
    ) -> PaginationResponse[Account]:

        filters = [pagination]

        results, total_count = await account_service.list_and_count(*filters)

        return PaginationResponse(
            data=list(results),
            total=total_count,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    @get(
        "/{account_id:uuid}",
        summary="賬戶詳情",
        responses={
            **COMMON_RESPONSES,
        },
        dto=AccountDTO,
    )
    async def get_account(
        self,
        account_service: AccountService,
        account_id: UUID,
    ) -> ApiResponse[Account]:
        result = await account_service.get(account_id)

        return ApiResponse(
            data=result,
            detail="賬戶詳情獲取成功",
        )
