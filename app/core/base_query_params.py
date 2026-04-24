from dataclasses import dataclass
from litestar.params import Parameter
from typing import Literal
from app.common.enums import SortBy


@dataclass
class QueryFilter:
    search: str | None = Parameter(default=None, description="搜索关键词")
    page: int = Parameter(ge=1, default=1)
    limit: Literal[10, 20, 50, 100] = Parameter(default=10)
    orderBy: str = Parameter(default="id")
    sortBy: SortBy = Parameter(default=SortBy.DESC)
