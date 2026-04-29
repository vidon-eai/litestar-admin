from contextlib import asynccontextmanager
import os
import click
from litestar import Litestar, Router
from litestar.openapi.config import OpenAPIConfig
from litestar.plugins import CLIPluginProtocol
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError
from app.common.exceptions import unified_exception_handler
from app.core.database import create_tables, seed_database, sqlalchemy_plugin


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


async def init_db() -> None:
    from app.core.logger import log
    from app.config.setting import get_settings

    settings = get_settings()
    try:
        await create_tables()
        log.info(f"✅ {settings.database_type}數據庫初始化完成")
    except OperationalError as e:
        log.error(f"❌ 資料庫連線失敗（請檢查資料庫是否運行、連線字串是否正確）: {e}")
        raise
    except ProgrammingError as e:
        log.error(f"❌ SQL 語法或權限錯誤: {e}")
        raise

    except SQLAlchemyError as e:
        log.error(f"❌ SQLAlchemy 錯誤: {e}")
        raise

    except Exception as e:  # 兜底捕捉其他未知異常
        log.critical(f"❌ 初始化資料庫時發生未預期錯誤: {e}", exc_info=True)
        raise  # 強烈建議在 startup 階段 raise，讓應用程式無法啟動


# @click.command()
# def seed_command() -> None:
#     """執行資料庫初始資料填充（只執行一次，不會每次重啟都跑）"""
#     asyncio.run(seed_database())   # 呼叫上面定義的 async function


@click.command(name="mycommand")
def mycommand(app: Litestar) -> None:
    """這是我的自定義命令"""
    click.echo(f"應用程式名稱: {app.__class__.__name__}")
    click.echo(f"Debug 模式: {app.debug}")
    click.echo("自定義命令執行成功！")

@asynccontextmanager
async def lifespan(app: Litestar):
    await init_db()
    # await seed_database()
    await on_startup(app)
    yield  # 應用程式正常運行
    
class CLIPlugin(CLIPluginProtocol):
    def on_cli_init(self, cli: click.Group) -> None:
        @cli.command(name="seed", help="Seed")
        async def seed(app: Litestar):
            await seed_database()

def create_app() -> Litestar:
    os.environ["ENVIRONMENT"] = "dev"

    from app.core.logger import setup_logging
    from app.api.register_routers import register_routers

    setup_logging()
    system_routers = register_routers()
    plugin_routers = register_routers("app.plugins")

    from app.config.setting import get_settings

    settings = get_settings()
    get_settings.cache_clear()
    
    return Litestar(
        debug=settings.debug,
        path=settings.root_path,
        route_handlers=[
            *system_routers,
            Router(path="/plugins", route_handlers=plugin_routers),
        ],
        openapi_config=OpenAPIConfig(
            title=settings.title,
            version=settings.version,
            description=settings.description,
            summary=settings.summary,
        ),
        # on_startup=[on_startup, init_db, seed_database],
        lifespan=[lifespan],
        plugins=[sqlalchemy_plugin, CLIPlugin()],
        exception_handlers={
            HTTP_404_NOT_FOUND: unified_exception_handler,
            HTTP_500_INTERNAL_SERVER_ERROR: unified_exception_handler,
            HTTP_400_BAD_REQUEST: unified_exception_handler,
        },
    )


if __name__ == "__main__":
    import uvicorn
    from app.core.logger import setup_logging

    from app.config.setting import get_settings

    settings = get_settings()
    get_settings.cache_clear()

    setup_logging()
    uvicorn.run(
        "main:create_app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
        factory=True,
        log_config=None,
    )
