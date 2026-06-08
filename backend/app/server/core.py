import sys
from advanced_alchemy.exceptions import IntegrityError, RepositoryError
from litestar import Litestar, Router
from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.plugins import InitPluginProtocol
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from app.common.exceptions import unified_exception_handler
from app.core.guards import auth
from app.core.dependencies import provide_user

async def find_routers(app: Litestar) -> None:
    from app.core.logger import log

    log.info("=" * 100)
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
                f"📍 {route_path:<35} | {http_method:<12} | {controller_name} ({handler_name})"
            )

    log.info("=" * 100)


async def db_connection() -> None:
    from app.core.logger import log
    from app.config.setting import app_setting

    try:
        async with app_setting.DB_CONFIG.get_engine().begin() as conn:
            await conn.execute(text("SELECT 1"))
        log.info("✅ 資料庫連接成功！")
    except Exception as e:
        log.info(f"❌ 資料庫連接失敗: {e}")
        log.info("🔴 程式將在 3 秒後退出...")

        import asyncio

        await asyncio.sleep(3)

        sys.exit(1)




class ApplicationCore(InitPluginProtocol):

    def on_app_init(self, app_config: AppConfig) -> AppConfig:

        from app.core.logger import setup_logging
        from app.api.register_routers import register_routers
        from app.core.database import sqlalchemy_plugin
        from app.core.middlewares import AuditLogMiddleware

        setup_logging()
        system_routers = register_routers()
        plugin_routers = register_routers("plugins")

        from app.config.setting import get_app_setting

        app_setting = get_app_setting()
        get_app_setting.cache_clear()

        app_config.on_startup.extend([db_connection, find_routers])
        app_config.debug = app_setting.DEBUG
        app_config.path = app_setting.ROOT_PATH
        app_config.route_handlers.extend(
            [
                *system_routers,
                Router(path="/plugins", route_handlers=plugin_routers),
            ]
        )
        app_config.openapi_config = OpenAPIConfig(
            title=app_setting.TITLE,
            version=app_setting.VERSION,
            description=app_setting.DESCRIPTION,
            summary=app_setting.SUMMARY,
            components=[auth.openapi_components],
            security=[auth.security_requirement],
        )
        app_config = auth.on_app_init(app_config)
        app_config.plugins.extend([sqlalchemy_plugin])

        app_config.exception_handlers = {
            HTTP_404_NOT_FOUND: unified_exception_handler,
            HTTP_500_INTERNAL_SERVER_ERROR: unified_exception_handler,
            HTTP_400_BAD_REQUEST: unified_exception_handler,
            HTTP_401_UNAUTHORIZED: unified_exception_handler,
            HTTP_403_FORBIDDEN: unified_exception_handler,
            IntegrityError: unified_exception_handler,
            RepositoryError: unified_exception_handler,
            OperationalError: unified_exception_handler,
        }

        app_config.dependencies.update(
            {
                "current_user": Provide(provide_user, sync_to_thread=False),
            }
        )
        app_config.middleware.append(AuditLogMiddleware())

        return super().on_app_init(app_config)
