import importlib
from abc import ABC, abstractmethod

from app.db.models.dataset import Dataset
from app.plugins.rag.vector_store.base_vector import BaseVector
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings

_BUILTIN_VECTOR_FACTORY_TARGETS = {
    "milvus": "app.plugins.rag.vector_store.milvus_vector:VectorFactory",
    "chroma": "app.plugins.rag.vector_store.chroma_vector:VectorFactory",
}


class AbstractVectorFactory(ABC):
    @abstractmethod
    def init_vector(self, dataset: Dataset, embeddings: Embeddings) -> BaseVector:
        raise NotImplementedError


def _load_builtin_factory(type: str) -> type[AbstractVectorFactory]:
    target = _BUILTIN_VECTOR_FACTORY_TARGETS.get(type)
    if not target:
        raise ValueError(f"Vector store {type!r} is not supported")
    module_path, _, attr = target.partition(":")
    module = importlib.import_module(module_path)

    return getattr(module, attr)


def get_vector_factory_class(type: str) -> type[AbstractVectorFactory]:

    return _load_builtin_factory(type)


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

    def delete_collection(self):
        self._vector_store.delete_collection()

    def delete_by_ids(self, ids: list[str]):
        self._vector_store.delete_by_ids(ids)
