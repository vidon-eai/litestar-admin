import sys
from advanced_alchemy.exceptions import IntegrityError, RepositoryError
from litestar import Litestar, Router
from litestar.config.app import AppConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.plugins import InitPluginProtocol
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

from app.common.exceptions import unified_exception_handler
# from app.core.database import db_config


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


async def db_connection() -> None:
    from app.config.setting import settings

    try:
        async with settings.db_config.get_engine().begin() as conn:
            # 執行簡單查詢測試連接
            await conn.execute(text("SELECT 1"))
            # 或使用 SELECT 1::int 等特定 dialect 的方式
        print("✅ 資料庫連接成功！")
    except Exception as e:
        print(f"❌ 資料庫連接失敗: {e}")
        print("🔴 程式將在 3 秒後退出...")
        
        # 等待一下讓錯誤訊息能被看到
        import asyncio
        await asyncio.sleep(3)
        
        # 退出程序，並返回非零錯誤碼
        sys.exit(1)  # 1 表示異常退出


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

        app_config.on_startup.extend([on_startup, db_connection])
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
            OperationalError: unified_exception_handler,
        }

        return super().on_app_init(app_config)
