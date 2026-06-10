from abc import ABC, abstractmethod
from opendal import Operator, AsyncOperator
from typing import Optional, List
import os


class AsyncStorageDriver(ABC):
    """文件存储抽象基类，统一规范所有存储驱动行为"""
    def __init__(self):
        pass

    @abstractmethod
    async def put(self, path: str, data: bytes) -> bool:
        """写入文件"""
        ...

    @abstractmethod
    async def get(self, path: str) -> Optional[bytes]:
        """读取文件"""
        ...

    @abstractmethod
    async def delete(self, path: str) -> bool:
        """删除文件"""
        ...

    @abstractmethod
    async def list(self, prefix: str = "") -> List[str]:
        """列举文件"""
        ...

    def validate_file(self, filename: str, file_size: int) -> tuple[bool, str]:
        """通用文件校验（大小、后缀）"""
        if file_size > self.max_size:
            return False, f"文件超出限制({self.max_size/1024/1024:.1f}MB)"
        if not filename.lower().endswith(self.allow_suffix):
            return False, f"仅支持 {self.allow_suffix} 格式"
        return True, "ok"


class OpenDALStorage(AsyncStorageDriver):
    def __init__(self, root_path: str = "./storage"):
        os.makedirs(root_path, exist_ok=True)
        self.operator = AsyncOperator(scheme="fs", root=root_path)

    async def put(self, file_path: str, data: bytes) -> tuple[bool, str | None]:
        try:
            await self.operator.write(file_path, data)
            return True, file_path
        except Exception as e:
            print(f"文件保存失败: {e}")
            return False, None

    async def get(self, file_path: str) -> Optional[bytes]:
        try:
            return await self.operator.read(file_path)
        except Exception:
            return None

    async def delete(self, file_path: str) -> bool:
        try:
            await self.operator.delete(file_path)
            return True
        except Exception:
            return False

    async def list(self, prefix: str = "") -> List[str]:
        try:
            entries = await self.operator.list(prefix)
            return [e.path for e in entries if not e.is_dir]
        except Exception:
            return []

    async def close(self) -> None:
        await self.operator.close()

class S3Storage(AsyncStorageDriver):
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
