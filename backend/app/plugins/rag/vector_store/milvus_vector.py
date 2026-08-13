import asyncio
from dataclasses import dataclass
from typing import Any

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_milvus import Milvus

from app.config.setting import app_setting
from app.core.logger import log


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
    def __init__(
        self, collection_name: str, config: MilvusConfig, embeddings: Embeddings
    ):
        self._config = config
        self._collection_name = collection_name

        if not embeddings:
            raise ValueError("Embeddings is required")

        self._embeddings = embeddings
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
        log.info("初始化 Milvus", self._embeddings, self._collection_name)
        return Milvus(
            embedding_function=self._embeddings,
            collection_name=self._collection_name,
            connection_args=connection_args,
            index_params=index_params,
            drop_old=config.drop_old,
            auto_id=config.auto_id,
            consistency_level=config.consistency_level,
        )

    def get_vector_store(self):
        return self._client

    async def aadd_documents(self, documents: list[Document]):
        batch_size = 30
        max_retries = 3
        cooldown = 0.5
        total_splits = len(documents)

        log.info(f"開始寫入 {total_splits} 個文本切片 (每批 {batch_size} 筆)...")
        pks: list[str] = []
        # 1. 批次切分迴圈，避免一次性拋送大量請求導致 Ollama 崩潰
        for i in range(0, total_splits, batch_size):
            batch = documents[i : i + batch_size]
            current_range = (
                f"{i + 1}-{min(i + batch_size, total_splits)}/{total_splits}"
            )

            # 2. 自動重試機制
            for attempt in range(1, max_retries + 1):
                try:
                    ids = await self._client.aadd_documents(batch)
                    pks.append(ids)
                    log.info(f"成功寫入批次 [{current_range}]")
                    break
                except Exception as e:
                    log.info(
                        f"寫入批次 [{current_range}] 失敗 (第 {attempt}/{max_retries} 次嘗試): {e}"
                    )
                    if attempt == max_retries:
                        log.info(f"批次 [{current_range}] 已達最大重試次數，拋出異常。")
                        raise e

                    # 指數級退讓等待，給 Ollama 內部進程恢復或清理記憶體的時間
                    wait_time = attempt * 2
                    log.info(f"等待 {wait_time} 秒後重新嘗試...")
                    await asyncio.sleep(wait_time)

            # 3. 每批次成功後短暫停頓，保護 GPU / 記憶體資源
            if cooldown > 0:
                await asyncio.sleep(cooldown)
        return pks

    def drop_vector(self):
        self._client.drop()
        
class MilvusVectorFactory:
    """
    Factory class for creating MilvusVector instances.
    """

    def init_vector(self, collection_name: str, embeddings: Embeddings) -> MilvusVector:

        return MilvusVector(
            embeddings=embeddings,
            collection_name=collection_name,
            config=MilvusConfig(
                uri=app_setting.MILVUS_URI,
                token=app_setting.MILVUS_TOKEN,
                user=app_setting.MILVUS_USER,
                password=app_setting.MILVUS_PASSWORD,
                database=app_setting.MILVUS_DATABASE,
                auto_id=app_setting.MILVUS_AUTO_ID,
                consistency_level=app_setting.MILVUS_CONSISTENCY_LEVEL,
                drop_old=app_setting.MILVUS_DROP_OLD,
            ),
        )
