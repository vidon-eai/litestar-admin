from abc import ABC


class BaseVectorStore(ABC):
    def __init__(self, collection_name: str):
        self._collection_name = collection_name

    @property
    def collection_name(self):
        return self._collection_name
