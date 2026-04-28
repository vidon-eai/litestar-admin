from enum import Enum, unique


@unique
class SortBy(str, Enum):
    ASC = "asc"
    DESC = "desc"
