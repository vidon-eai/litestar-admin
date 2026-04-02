from litestar import Controller
from litestar.di import Provide

from .base_query_params import QueryFilter


class BaseController(Controller):
    pass
