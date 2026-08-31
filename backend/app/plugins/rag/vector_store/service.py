from typing import TYPE_CHECKING

from app.db.models.dataset import Dataset
from app.plugins.rag.vector_store.vector_factory import Vector
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

if TYPE_CHECKING:
    from .config import VectorStoreConfig


class VectorStoreService:
    def __init__(self, config: "VectorStoreConfig"):
        self._config = config
        self._embedding_model = self._config.embedding_model

    def get_embedding(self, provider: str) -> OllamaEmbeddings:
        return OllamaEmbeddings(model=provider)

    def get_retriever(self, dataset: Dataset, **kwargs):
        vector = Vector(dataset=dataset, embedding_model=self._embedding_model)

        search_type = kwargs.get("search_type", "similarity")
        search_kwargs = kwargs.get("search_kwargs", {"k": 4})

        retriever = vector.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs,
        )
        return retriever

    async def embed(self, dataset: Dataset, docs: list[Document], index_ids: list[str]):
        vector = Vector(dataset=dataset, embedding_model=self._embedding_model)
        return await vector.aadd_documents(docs, index_ids=index_ids)

    def delete_collection(self, dataset: Dataset):
        vector_store = Vector(dataset=dataset, embedding_model=self._embedding_model)
        vector_store.delete_collection()

    def delete_by_ids(self, dataset: Dataset, ids: list[str]):
        vector_store = Vector(dataset=dataset, embedding_model=self._embedding_model)
        vector_store.delete_by_ids(ids)
