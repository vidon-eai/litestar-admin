from contextlib import asynccontextmanager

from app.cli.commands import cli
from app.plugins.storage.plugin import StoragePlugin
from app.utils.route_log import RouteLoggerPlugin
from litestar import Litestar


@asynccontextmanager
async def spy_on_plugins(app: Litestar):
    # 應用啟動時觸發，此時 app.plugins 已經是唯讀且完全確定的狀態
    print("🚀 應用已啟動，最終載入的插件清單為：")
    for plugin in app.plugins:
        tag = getattr(plugin, "plugin_tag", None)
        if tag:
            print(f" - {type(plugin).__name__} (tag: {tag})")
    yield


def create_app() -> Litestar:
    from app.server.core import ApplicationCore
    return Litestar(
        plugins=[ApplicationCore(), StoragePlugin(), RouteLoggerPlugin()],
    )


if __name__ == "__main__":
    cli()
