from enum import Enum, StrEnum, unique


@unique
class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


@unique
class SortFields(StrEnum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class StorageTypeEnum(StrEnum):
    S3 = "s3"
    LOCAL = "local"
    FS = "fs"
