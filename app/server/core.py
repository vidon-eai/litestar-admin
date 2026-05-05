
import os
from advanced_alchemy.exceptions import IntegrityError, RepositoryError
from litestar import Litestar, Router
from litestar.config.app import AppConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.plugins import InitPluginProtocol
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.exc import OperationalError

from app.common.exceptions import unified_exception_handler


async def on_startup(app: Litestar) -> None:
    from app.core.logger import log

    sorted_routes = app.route_handler_method_map.items()
    for route_path, method_map in sorted_routes:

        if route_path == "/api/v1/schema" or route_path.startswith("/api/v1/schema"):
            continue

        for http_method, handler in method_map.items():
            if http_method == "OPTIONS":
                continue
            controller_part, handler_name = str(handler).rsplit(".", 1)
            controller_name = controller_part.rsplit(".", 1)[-1]
            log.info(
                f"[{http_method:<6}] {route_path:<35} - {controller_name}:{handler_name}"
            )


class ApplicationCore(InitPluginProtocol):

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        
        from app.core.logger import setup_logging
        from app.api.register_routers import register_routers
        from app.core.database import sqlalchemy_plugin

        setup_logging()
        system_routers = register_routers()
        plugin_routers = register_routers("plugins")

        from app.config.setting import get_settings

        settings = get_settings()
        get_settings.cache_clear()

        app_config.on_startup.extend([on_startup])
        app_config.debug = settings.debug
        app_config.path = settings.root_path
        app_config.route_handlers.extend(
            [
                *system_routers,
                Router(path="/plugins", route_handlers=plugin_routers),
            ]
        )
        app_config.openapi_config = OpenAPIConfig(
            title=settings.title,
            version=settings.version,
            description=settings.description,
            summary=settings.summary,
        )

        app_config.plugins.extend([sqlalchemy_plugin])

        app_config.exception_handlers = {
            HTTP_404_NOT_FOUND: unified_exception_handler,
            HTTP_500_INTERNAL_SERVER_ERROR: unified_exception_handler,
            HTTP_400_BAD_REQUEST: unified_exception_handler,
            IntegrityError: unified_exception_handler,
            RepositoryError: unified_exception_handler,
            OperationalError: unified_exception_handler
        }

        return super().on_app_init(app_config)