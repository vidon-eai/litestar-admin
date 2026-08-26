from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseLoader(ABC):
    @abstractmethod
    def parse(self, source_path: str, **kwargs) -> list[Document]:
        raise NotImplementedError
