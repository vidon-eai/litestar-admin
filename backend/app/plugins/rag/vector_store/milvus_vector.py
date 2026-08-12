from dataclasses import dataclass
from typing import Any

from app.plugins.rag.vector_store.vector_base import BaseVectorStore
from langchain_core.embeddings import Embeddings
from langchain_milvus import Milvus


@dataclass
class MilvusConfig:
    """
    Configuration class for Milvus connection.
    """

    uri: str  # Milvus server URI
    token: str | None = None  # Optional token for authentication
    user: str | None = None  # Username for authentication
    password: str | None = None  # Password for authentication
    database: str = "default"  # Database name

    drop_old: bool = False
    auto_id: bool = True
    consistency_level: str = "Strong"
    embeddings: Embeddings | None = None

    def __post_init__(self):
        """
        Validate the configuration values after initialization.
        Raises ValueError if required fields are missing.
        """
        if not self.uri:
            raise ValueError("config MILVUS_URI is required")
        if not self.token:
            if not self.user:
                raise ValueError("config MILVUS_USER is required")
            if not self.password:
                raise ValueError("config MILVUS_PASSWORD is required")


class MilvusVector(BaseVectorStore):
    def __init__(self, collection_name: str, config: MilvusConfig):
        super().__init__(collection_name)
        self._config = config
        self._client = self._init_client(config)

    def _init_client(self, config: MilvusConfig) -> Milvus:
        """
        Initialize and return a Milvus client.
        """
        connection_args: dict[str, Any] = {
            "uri": config.uri,
            "db_name": config.database,
        }
        if config.token:
            connection_args["token"] = config.token
        else:
            connection_args["user"] = config.user or ""
            connection_args["password"] = config.password or ""

        index_params = {"index_type": "FLAT", "metric_type": "L2"}
        print("Vector Config:", config)
        return Milvus(
            embedding_function=config.embeddings,
            connection_args=connection_args,
            index_params=index_params,
            drop_old=config.drop_old,
            # auto_id=config.auto_id,
            consistency_level=config.consistency_level,
        )

    def get_vector_store(self):
        return self._client
