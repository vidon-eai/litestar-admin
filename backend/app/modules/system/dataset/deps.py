from typing import Annotated, Literal

from app.common.enums import SortBy, SortFields
from app.core.dependencies import build_query_filters
from litestar.params import Parameter

QUERY_ORDER_BY = "orderBy"
QUERY_SORT_ORDER = "sortOrder"
PAGE_SIZE = Literal[10, 20, 30, 50]


def provide_dataset_filters(
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

    return build_query_filters(
        page=page,
        page_size=page_size,
        search=search,
        search_fields=["name", "description"],
        order_by=order_by,
        sort_order=sort_order,
    )
