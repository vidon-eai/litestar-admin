import asyncio
from dataclasses import dataclass
from typing import Any

import chromadb
from app.core.logger import log
from app.db.models.dataset import Dataset
from app.plugins.rag.vector_store.base_vector import BaseVector
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


@dataclass
class ChromaConfig:
    """
    Configuration class for Milvus connection.
    """

    type: str = "local"

    # Running locally
    path: str | None = None

    # Running Chroma server
    host: str | None = None
    port: int | None = None
    ssl: bool = False


class ChromaVector(BaseVector):
    def __init__(
        self, collection_name: str, config: ChromaConfig, embeddings: Embeddings
    ):
        self._config = config
        self._collection_name = collection_name

        if not embeddings:
            raise ValueError("Embeddings is required")

        self._embeddings = embeddings

        self._client = self._init_client(config)

    def _init_client(self, config: ChromaConfig) -> Chroma:
        """
        Initialize and return a Chroma client.
        """

        if config.type == "local":
            if config.path:
                client = chromadb.PersistentClient(path=config.path)
        elif config.type == "server":
            if config.host and config.port:
                client = chromadb.HttpClient(
                    host=config.host, port=config.port, ssl=config.ssl
                )

        log.info("初始化 Chroma", self._embeddings, self._collection_name)
        return Chroma(
            client=client,
            embedding_function=self._embeddings,
            collection_name=self._collection_name,
        )

    def get_vector_store(self):
        return self._client

    async def aadd_documents(self, documents: list[Document], **kwargs: Any):
        batch_size = 30
        max_retries = 3
        cooldown = 0.5
        total_splits = len(documents)
        index_ids = kwargs.get("index_ids", [])
        log.info(f"開始寫入 {total_splits} 個文本切片 (每批 {batch_size} 筆)...")
        pks: list[str] = []
        # 1. 批次切分迴圈，避免一次性拋送大量請求導致 Ollama 崩潰
        for i in range(0, total_splits, batch_size):
            batch = documents[i : i + batch_size]
            batch_ids = index_ids[i : i + batch_size]
            current_range = (
                f"{i + 1}-{min(i + batch_size, total_splits)}/{total_splits}"
            )

            # 2. 自動重試機制
            for attempt in range(1, max_retries + 1):
                try:
                    ids = await self._client.aadd_documents(batch, ids=batch_ids)
                    pks.extend(ids)
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

    def delete_collection(self):
        self._client.delete_collection()

    def delete_by_ids(self, index_ids: list[str]):
        return self._client.delete(index_ids)

    async def asimilarity_search_with_score(self, query: str, k: int):
        return await self._client.asimilarity_search_with_score(query, k=k)

    def retriever(self, **kwargs):
        return self._client.as_retriever(**kwargs)


class VectorFactory:
    """
    Factory class for creating MilvusVector instances.
    """

    def init_vector(self, dataset: Dataset, embeddings: Embeddings) -> ChromaVector:

        collection_name = dataset.vector_index_name

        return ChromaVector(
            embeddings=embeddings,
            collection_name=collection_name,
            config=ChromaConfig(type="local", path="./vector_db"),
        )
