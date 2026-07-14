from enum import Enum, StrEnum, unique


@unique
class SortBy(str, Enum):
    ASC = "asc"
    DESC = "desc"


class StatusEnum(StrEnum):
    VALID = "1"
    INVALID = "0"


class StorageTypeEnum(StrEnum):
    S3 = "s3"
    LOCAL = "local"
    FS = "fs"
