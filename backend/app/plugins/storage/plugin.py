from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPluginProtocol

from .config import StorageConfig


class StoragePlugin(InitPluginProtocol):
    plugin_tag = "storage"

    def __init__(self, config: "StorageConfig | None" = None) -> None:
        self._config = config or StorageConfig()

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.lifespan.append(self._config.lifespan)
        app_config.dependencies.update(
            {
                self._config.storage_dependency_key: Provide(
                    self._config.provide_storage, sync_to_thread=False
                ),
            }
        )

        return app_config
