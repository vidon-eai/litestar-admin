import importlib
from abc import ABC, abstractmethod

from app.db.models.dataset import Dataset
from app.plugins.rag.vector_store.base_vector import BaseVector
from langchain.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings


class AbstractVectorFactory(ABC):
    @abstractmethod
    def init_vector(self, dataset: Dataset, embeddings: Embeddings) -> BaseVector:
        raise NotImplementedError


def get_vector_factory_class(vector_type: str) -> type[AbstractVectorFactory]:

    module_name = f"app.plugins.rag.vector_store.{vector_type}_vector"

    module = importlib.import_module(module_name)

    factory_class = getattr(module, "VectorFactory")

    return factory_class


class Vector:
    def __init__(self, dataset: Dataset, embedding_model: str):
        self._embeddings = OllamaEmbeddings(model=embedding_model)
        self._dataset = dataset
        self._vector_store = self._init_vector()

    def _init_vector(self) -> BaseVector:
        vector_factory_cls = self.get_vector_factory("milvus")
        return vector_factory_cls().init_vector(self._dataset, self._embeddings)

    @staticmethod
    def get_vector_factory(vector_type: str) -> type[AbstractVectorFactory]:
        return get_vector_factory_class(vector_type)

    async def aadd_documents(self, documents: list[Document], **kwargs):
        return await self._vector_store.aadd_documents(documents=documents, **kwargs)

    def as_retriever(self, **kwargs):
        return self._vector_store.retriever(**kwargs)
