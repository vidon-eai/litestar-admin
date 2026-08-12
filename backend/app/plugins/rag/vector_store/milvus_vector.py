from dataclasses import dataclass
from typing import Any

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


class MilvusVector:
    def __init__(self, config: MilvusConfig):
        self._config = config
        self._client = self._init_client(config)

    def _init_client(self, config: MilvusConfig) -> Milvus:
        """
        Initialize and return a Milvus client.
        """
        kwargs: dict[str, Any] = {"uri": config.uri, "db_name": config.database}
        if config.token:
            kwargs["token"] = config.token
        else:
            kwargs["user"] = config.user or ""
            kwargs["password"] = config.password or ""
        if config.secure:
            kwargs["secure"] = True
            if config.server_pem_path:
                kwargs["server_pem_path"] = config.server_pem_path
            if config.server_name:
                kwargs["server_name"] = config.server_name
        return Milvus(**kwargs)
