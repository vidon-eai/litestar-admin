from enum import Enum, unique


@unique
class SortBy(Enum):
    ASC = "asc"
    DESC = "desc"
