from abc import ABC, abstractmethod


class AsyncStorageDriver(ABC):
    """Interface for file storage."""

    @abstractmethod
    async def put(self, path: str, data: bytes):
        raise NotImplementedError

    @abstractmethod
    async def get(self, path: str):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, path: str):
        raise NotImplementedError
