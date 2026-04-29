from enum import Enum
from typing import Annotated, Literal, Sequence, Type, TypeVar
from advanced_alchemy.filters import (
    ComparisonFilter,
    LimitOffset,
    OrderBy,
    SearchFilter,
)
from litestar.params import Parameter
from app.common.enums import SortBy

async def provide_pagination(
    page: Annotated[int, Parameter(ge=1, default=1, description="頁碼")],
    page_size: Annotated[
        Literal[10, 20, 30, 50],
        Parameter(query="pageSize", default=10, description="每頁數量"),
    ],
) -> LimitOffset:
    return LimitOffset(limit=page_size, offset=(page - 1) * page_size)

def create_search_provider(field_names: Sequence[str]):
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
def create_order_provider(order_enum: Type[T], default_field: str | None = None):
    """
    排序工廠：支持動態傳入 Enum 並處理默認排序
    """

    async def provide_order(
        order_by: Annotated[
            order_enum | None, Parameter(query="orderBy", default=None)
        ] = None,
        sort_order: Annotated[
            SortBy, Parameter(query="sortOrder", default=SortBy.DESC)
        ] = SortBy.DESC,
    ) -> OrderBy | None:
        field = order_by.value if order_by else default_field
        if not field:
            return None
        return OrderBy(field_name=field, sort_order=sort_order.value)

    return provide_order
    
async def provide_filter_list(
    is_active: bool | None = Parameter(query="isActive", default=None, description="激活狀態"),
    description: str | None = Parameter(query="description", default=None, description="用戶描述"),
) -> list[ComparisonFilter]:
    """
    根據傳入的查詢參數，動態構建 ComparisonFilter 列表
    """
    filters: list[ComparisonFilter] = []
    
    if is_active is not None:
        filters.append(ComparisonFilter(field_name="is_active", operator="eq", value=is_active))
        
    if description is not None:
        filters.append(ComparisonFilter(field_name="description", operator="eq", value=description))
        
    return filters