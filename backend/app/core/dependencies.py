from enum import Enum
from typing import Annotated, Any, Literal, Sequence, Type, TypeVar

from advanced_alchemy.filters import (
    ComparisonFilter,
    FilterTypes,
    LimitOffset,
    OrderBy,
    SearchFilter,
)
from app.common.enums import SortBy
from app.db.models import User
from litestar import Request
from litestar.params import Parameter
from litestar.security.jwt import Token


async def create_pagination_provider(
    page: Annotated[int, Parameter(ge=1, default=1, description="頁碼")],
    page_size: Annotated[
        Literal[10, 20, 30, 50],
        Parameter(query="pageSize", default=10, description="每頁數量"),
    ],
) -> LimitOffset:
    return LimitOffset(limit=page_size, offset=(page - 1) * page_size)


def create_search_provider(field_names: set[str]):
    """
    搜索工廠：根據傳入的字段列表生成專用的 SearchFilter Provider
    """

    async def provide_search(
        search: Annotated[
            str | None, Parameter(description="模糊查詢", required=False)
        ] = None,
    ) -> SearchFilter | None:
        if not search:
            return None

        return SearchFilter(
            field_name=field_names,  # 這裡使用工廠傳入的動態字段
            value=search,
            ignore_case=True,
        )

    return provide_search


T = TypeVar("T", bound=Enum)

QUERY_ORDER_BY = "orderBy"
QUERY_SORT_ORDER = "sortOrder"


def create_order_provider(order_enum: Type[T], default_field: str | None = None):
    """
    排序工廠：支持動態傳入 Enum 並處理默認排序
    """

    async def provide_order(
        order_by: Annotated[order_enum, Parameter(query=QUERY_ORDER_BY, default=None)],
        sort_order: Annotated[
            SortBy, Parameter(query=QUERY_SORT_ORDER, default=SortBy.DESC)
        ],
    ) -> OrderBy | None:
        field = order_by.value if order_by else default_field
        if not field:
            return None
        return OrderBy(field_name=field, sort_order=sort_order.value)

    return provide_order


async def provide_filter_list(
    is_active: bool | None = Parameter(
        query="isActive", default=None, description="激活狀態"
    ),
    description: str | None = Parameter(
        query="description", default=None, description="用戶描述"
    ),
) -> list[ComparisonFilter]:
    """
    根據傳入的查詢參數，動態構建 ComparisonFilter 列表
    """
    filters: list[ComparisonFilter] = []

    if is_active is not None:
        filters.append(
            ComparisonFilter(field_name="is_active", operator="eq", value=is_active)
        )

    if description is not None:
        filters.append(
            ComparisonFilter(field_name="description", operator="eq", value=description)
        )

    return filters


def provide_user(request: Request[User, Token, Any]) -> Any:
    """Get the user from the connection.

    Args:
        request: current connection.

    Returns:
        User
    """
    return request.user


def build_query_filters(
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    search_fields: Sequence[str] = ("name", "description"),
    order_by: Enum | str | None = None,
    sort_order: SortBy | None = None,
    exact_matches: list[tuple[str, str, Any]] | None = None,
    custom_filters: list[Any] | None = None,
) -> list[FilterTypes]:
    filters: list[FilterTypes] = []

    # 1. 模糊搜索
    if search and search_fields:
        filters.append(SearchFilter(field_name=list(search_fields), value=search))

    # 2. 精准匹配列表 (field_name, operator, value)
    if exact_matches:
        for field_name, op, val in exact_matches:
            if val is not None:
                filters.append(
                    ComparisonFilter(field_name=field_name, operator=op, value=val)
                )

    # 3. 排序
    if order_by and sort_order:
        field_val = order_by.value if isinstance(order_by, Enum) else order_by
        filters.append(OrderBy(field_name=field_val, sort_order=sort_order.value))

    # 4. 自定义拓展的复杂 Filter 实例
    if custom_filters:
        filters.extend(custom_filters)

    # 5. 分页
    filters.append(LimitOffset(limit=page_size, offset=(page - 1) * page_size))

    return filters
