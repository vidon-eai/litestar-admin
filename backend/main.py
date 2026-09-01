from contextlib import asynccontextmanager

from app import plugins
from app.cli.commands import cli
from app.common.enums import StorageTypeEnum
from litestar import Litestar
from litestar.config.cors import CORSConfig


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

    storage_config = {
        "storage_type": app_setting.STORAGE_TYPE,
        "storage_scheme": app_setting.STORAGE_SCHEME,
    }

    if app_setting.STORAGE_TYPE == StorageTypeEnum.S3:
        storage_config.update(
            {
                "endpoint": app_setting.S3_ENDPOINT,
                "bucket": app_setting.S3_BUCKET_NAME,
                "access_key": app_setting.S3_ACCESS_KEY,
                "secret_access_key": app_setting.S3_SECRET_KEY,
                "region": app_setting.S3_REGION,
            }
        )
    else:
        storage_config.update({"root_path": app_setting.STORAGE_PATH})

    from app.core.application import ApplicationCore

    return Litestar(
        plugins=[
            ApplicationCore(),
            plugins.StoragePlugin(config=StorageConfig(**storage_config)),
            plugins.RAGPlugin(),
            plugins.RouteLoggerPlugin(),
        ],
        cors_config=CORSConfig(),
    )


if __name__ == "__main__":
    cli()
