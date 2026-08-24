from __future__ import annotations

from abc import ABC, abstractmethod

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


class BaseVector(ABC):
    def __init__(self, collection_name: str):
        self._collection_name = collection_name

    @abstractmethod
    async def aadd_documents(self, documents: list[Document], **kwargs) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def delete_collection(self):
        raise NotImplementedError

    @abstractmethod
    def delete_by_ids(self, ids: list[str]):
        raise NotImplementedError

    @abstractmethod
    def retriever(self) -> VectorStoreRetriever:
        raise NotImplementedError

    @abstractmethod
    def similarity_search(self, query: str, top_k: int, **kwargs) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    async def asimilarity_search(
        self, query: str, top_k: int, **kwargs
    ) -> list[Document]:
        raise NotImplementedError

    @property
    def collection_name(self):
        return self._collection_name
