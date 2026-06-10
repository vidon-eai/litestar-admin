from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import BinaryIO
from pathlib import Path
from opendal import Operator

class BaseStorage(ABC):

    @abstractmethod
    def save(self, file_path: str, data: bytes):
       raise NotImplementedError

    # @abstractmethod
    # async def get_file_url(self, file_path: str) -> str:
    #     raise NotImplementedError

    # @abstractmethod
    # async def delete(self, file_path: str) -> bool:
    #     raise NotImplementedError

    # @abstractmethod
    # async def exists(self, file_path: str) -> bool:
    #     raise NotImplementedError


class OpenDALStorage(BaseStorage):
    def __init__(self, scheme: str, **kwargs):

        if scheme == "fs":
            root = kwargs.setdefault("root", "storage")
            Path(root).mkdir(parents=True, exist_ok=True)

        self.op = Operator(scheme=scheme, **kwargs)
    
    def save(self, file_path: str, data: bytes) -> tuple[bool, str]:
        self.op.write(file_path, data)
        return True, file_path
    
    def get_file_url(self, file_path: str) -> str:
        return self.op.read(file_path)
    
    def delete(self, file_path: str) -> bool:
        if(self.exists(file_path)):
            self.op.delete(file_path)
        return True
    
    def exists(self, file_path: str) -> bool:
        return self.op.exists(file_path)

class S3Storage(BaseStorage):
    def __init__(self, bucket_name: str = 'storage'):
        print("S3Storage initialized")
        self.bucket_name = bucket_name
    
    def save(self, file_path: str, data: bytes) -> tuple[bool, str]:
        return True, file_path
    
    def get_file_url(self, file_path: str) -> str:
        pass
    
    def delete(self, file_path: str) -> bool:
        pass
    
    def exists(self, file_path: str) -> bool:
        pass


class Storage:
    @staticmethod
    def get_storage_factory(storage_type: str) -> Callable[[], BaseStorage]:
        match storage_type:
            case "fs":
                return lambda: OpenDALStorage("fs")
            case "s3":
                return S3Storage
            case _:
                raise ValueError(f"unsupported storage type {storage_type}")