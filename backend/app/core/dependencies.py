from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Annotated, Any, Literal

from advanced_alchemy.filters import (
    ComparisonFilter,
    FilterTypes,
    LimitOffset,
    OrderBy,
    SearchFilter,
)
from app.common.enums import SortBy, SortFields
from app.db.models import User
from litestar import Request
from litestar.params import Parameter
from litestar.security.jwt import Token


def provide_user(request: Request[User, Token, Any]) -> Any:
    """Get the user from the connection.

    Args:
        request: current connection.

    Returns:
        User
    """
    return request.user


@dataclass(slots=True, frozen=True)
class ComparisonCondition:
    field: str
    operator: str  # 或改成 Enum，例如 ComparisonOp
    value: Any

    def to_filter(self) -> ComparisonFilter:
        return ComparisonFilter(
            field_name=self.field,
            operator=self.operator,
            value=self.value,
        )


@dataclass(slots=True)
class QueryFilterParams:
    """查詢參數的集中承載物件，避免函式參數過多。"""

    page: int = 1
    page_size: int = 10
    search: str | None = None
    search_fields: Sequence[str] = ("name", "description")
    order_by: SortFields | str | None = None
    sort_order: SortBy | None = None
    custom_filters: list[FilterTypes] = field(default_factory=list)
    comparison_conditions: list[ComparisonCondition] = field(default_factory=list)
    enable_pagination: bool = True
    max_page_size: int = 100

    def normalized(self) -> QueryFilterParams:
        """回傳邊界校正後的新實例（immutable 風格）。"""
        page = max(self.page, 1)
        page_size = max(1, min(self.page_size, self.max_page_size))
        return QueryFilterParams(
            page=page,
            page_size=page_size,
            search=self.search,
            search_fields=self.search_fields or ("name", "description"),
            order_by=self.order_by,
            sort_order=self.sort_order,
            custom_filters=list(self.custom_filters),
            comparison_conditions=list(self.comparison_conditions),
            enable_pagination=self.enable_pagination,
            max_page_size=self.max_page_size,
        )


def build_query_filters(params: QueryFilterParams) -> list[FilterTypes]:
    """
    根據參數物件組裝 FilterTypes 列表。
    職責單一：只負責把「已正規化的參數」轉成 filter 列表。
    """
    p = params.normalized()
    filters: list[FilterTypes] = []

    # 1. 全文 / 模糊搜尋
    if p.search and p.search_fields:
        filters.append(SearchFilter(field_name=set(p.search_fields), value=p.search))

    # 2. 比較條件
    for cond in p.comparison_conditions:
        if cond.value is not None:
            filters.append(cond.to_filter())

    # 3. 排序（必須同時有欄位與方向）
    if p.order_by is not None and p.sort_order is not None:
        field_name = p.order_by.value if isinstance(p.order_by, Enum) else p.order_by
        filters.append(OrderBy(field_name=field_name, sort_order=p.sort_order.value))

    # 4. 自訂過濾器
    filters.extend(p.custom_filters)

    # 5. 分頁
    if p.enable_pagination:
        offset = (p.page - 1) * p.page_size
        filters.append(LimitOffset(limit=p.page_size, offset=offset))

    return filters


QUERY_ORDER_BY = "orderBy"
QUERY_SORT_ORDER = "sortOrder"
PAGE_SIZE = Literal[10, 20, 30, 50]


def provide_filters(
    page: Annotated[int, Parameter(ge=1, default=1, description="頁碼")] = 1,
    page_size: Annotated[
        PAGE_SIZE,
        Parameter(query="pageSize", default=10, description="每頁數量"),
    ] = 10,
    search: Annotated[
        str | None, Parameter(description="模糊查詢", required=False)
    ] = None,
    order_by: Annotated[
        SortFields | None,
        Parameter(query=QUERY_ORDER_BY, description="字段排序", required=False),
    ] = None,
    sort_order: Annotated[
        SortBy | None,
        Parameter(query=QUERY_SORT_ORDER, description="排序", required=False),
    ] = None,
):

    params = QueryFilterParams(
        page=page,
        page_size=page_size,
        search=search,
        search_fields=["name", "description"],  # 這裡仍可客製
        order_by=order_by,
        sort_order=sort_order,
    )
    return build_query_filters(params)
