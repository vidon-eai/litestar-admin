from app.plugins.rag.parsing.config import ParserConfig
from app.plugins.rag.vector_store.config import VectorStoreConfig
from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPluginProtocol

from .config import RAGConfig


class RAGPlugin(InitPluginProtocol):
    plugin_tag = "rag"

    def __init__(self, config: "RAGConfig | None" = None) -> None:
        self._config = config or RAGConfig()
        self._vector_store_config = VectorStoreConfig()
        self._parser_config = ParserConfig()

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.lifespan.append(self._config.lifespan)
        app_config.lifespan.append(self._vector_store_config.lifespan)
        app_config.lifespan.append(self._parser_config.lifespan)
        app_config.dependencies.update(
            {
                self._config.dependency_key: Provide(
                    self._config.provide_service, sync_to_thread=False
                ),
                self._vector_store_config.dependency_key: Provide(
                    self._vector_store_config.provide_service, sync_to_thread=False
                ),
                self._parser_config.dependency_key: Provide(
                    self._parser_config.provide_service, sync_to_thread=False
                ),
            }
        )

        return app_config
