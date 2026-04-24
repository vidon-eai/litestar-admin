
from advanced_alchemy.extensions.litestar import base


class Base(base.UUIDAuditBase):
    __abstract__ = True