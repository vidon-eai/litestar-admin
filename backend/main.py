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
    from app.config.setting import app_setting
    from app.plugins.storage.config import StorageConfig
    from app.server.core import ApplicationCore
    return Litestar(
        plugins=[ApplicationCore(), StoragePlugin(
            config=StorageConfig(
                root_path=app_setting.STORAGE_PATH,
                storage_type=app_setting.STORAGE_TYPE,
                endpoint=app_setting.S3_ENDPOINT,
                bucket=app_setting.S3_BUCKET_NAME,
                access_key=app_setting.S3_ACCESS_KEY,
                secret_access_key=app_setting.S3_SECRET_KEY,
                region=app_setting.S3_REGION
            )
        ), RouteLoggerPlugin()],
    )


if __name__ == "__main__":
    cli()
