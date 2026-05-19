
from advanced_alchemy.extensions.litestar import base


class Base(base.UUIDv7AuditBase):
    __abstract__ = True