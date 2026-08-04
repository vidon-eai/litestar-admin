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
from app.common.enums import SortFields, SortOrder
from app.db.models import User
from litestar import Request
from litestar.params import Parameter
from litestar.security.jwt import Token


def provide_user(request: Request[User, Token, Any]) -> Any:
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
    page: int = 1
    page_size: int = 10
    search: str | None = None
    search_fields: Sequence[str] = ("name", "description")
    sort_by: Enum | None = None
    sort_order: Enum | None = None
    custom_filters: list[FilterTypes] = field(default_factory=list)
    comparison_conditions: list[ComparisonCondition] = field(default_factory=list)


def build_query_filters(params: QueryFilterParams) -> list[FilterTypes]:
    filters: list[FilterTypes] = []

    if params.search and params.search_fields:
        filters.append(
            SearchFilter(field_name=set(params.search_fields), value=params.search)
        )

    for cond in params.comparison_conditions:
        if cond.field and cond.operator and cond.value is not None:
            filters.append(cond.to_filter())

    if params.sort_by is not None and params.sort_order is not None:
        field_name = (
            params.sort_by.value if isinstance(params.sort_by, Enum) else params.sort_by
        )
        sort_order = (
            params.sort_order.value
            if isinstance(params.sort_order, Enum)
            else params.sort_order
        )
        filters.append(OrderBy(field_name=field_name, sort_order=sort_order))

    filters.extend(params.custom_filters)

    if params.page is not None and params.page_size is not None:
        offset = (params.page - 1) * params.page_size
        filters.append(LimitOffset(limit=params.page_size, offset=offset))

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
    sort_by: Annotated[
        SortFields | None,
        Parameter(query=QUERY_ORDER_BY, description="字段排序", required=False),
    ] = None,
    sort_order: Annotated[
        SortOrder | None,
        Parameter(query=QUERY_SORT_ORDER, description="排序", required=False),
    ] = None,
):

    params = QueryFilterParams(
        page=page,
        page_size=page_size,
        search=search,
        search_fields=["name", "description"],  # 這裡仍可客製
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return build_query_filters(params)


__all__ = ["provide_user", "provide_filters"]
