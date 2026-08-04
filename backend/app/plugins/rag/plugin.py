from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPluginProtocol

from .config import RAGConfig


class RAGPlugin(InitPluginProtocol):
    plugin_tag = "rag"

    def __init__(self, config: "RAGConfig | None" = None) -> None:
        self._config = config or RAGConfig()

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.lifespan.append(self._config.lifespan)
        app_config.dependencies.update(
            {
                self._config.dependency_key: Provide(
                    self._config.provide_service, sync_to_thread=False
                ),
            }
        )

        return app_config
