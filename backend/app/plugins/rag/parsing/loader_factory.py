import importlib
from abc import ABC, abstractmethod

from app.plugins.rag.parsing.base_loader import BaseLoader

_BUILTIN_LOADER_FACTORY_TARGETS = {
    "pymupdf4llm": "app.plugins.rag.parsing.pymupdf4llm.loader:LoaderFactory",
    "docling": "app.plugins.rag.parsing.docling.loader:LoaderFactory",
}


class AbstractLoaderFactory(ABC):
    @abstractmethod
    def init_loader(self) -> BaseLoader:
        raise NotImplementedError


def _load_builtin_factory(type: str) -> type[AbstractLoaderFactory]:
    target = _BUILTIN_LOADER_FACTORY_TARGETS.get(type)
    if not target:
        raise ValueError(f"Loader {type!r} is not supported")
    module_path, _, attr = target.partition(":")
    module = importlib.import_module(module_path)

    return getattr(module, attr)


def get_loader_factory_class(type: str) -> type[AbstractLoaderFactory]:

    return _load_builtin_factory(type)


class Loader:
    def __init__(self, type: str = "docling"):
        self._type = type
        self._loader = self._init_loader()

    def _init_loader(self) -> BaseLoader:
        vector_factory_cls = self.get_loader_factory(self._type)
        return vector_factory_cls().init_loader()

    @staticmethod
    def get_loader_factory(type: str) -> type[AbstractLoaderFactory]:
        return get_loader_factory_class(type)

    def parse(self, soruce_path: str):
        return self._loader.parse(soruce_path)
