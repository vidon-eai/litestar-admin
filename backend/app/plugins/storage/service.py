from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

from opendal import AsyncOperator

if TYPE_CHECKING:
    from .config import StorageConfig


class StorageService:
    """
    A service class for handling storage operations.
    """

    def __init__(self, config: "StorageConfig | None" = None) -> None:
        root_path = config.root_path if config else "./storage"
        Path(root_path).mkdir(parents=True, exist_ok=True)
        self.op = AsyncOperator(scheme="fs", root=root_path)

    async def put(self, file_path: str, data: bytes) -> tuple[bool, str | None]:
        try:
            await self.op.write(file_path, data)
            return True, file_path
        except Exception as e:
            print(f"文件保存失败: {e}")
            return False, None

    async def get(self, file_path: str) -> Optional[bytes]:
        try:
            return await self.op.read(file_path)
        except Exception:
            return None

    async def delete(self, file_path: str) -> bool:
        try:
            await self.op.delete(file_path)
            return True
        except Exception:
            return False

    async def list(self, prefix: str = "") -> List[str]:
        try:
            entries = await self.op.list(prefix)
            return [e.path for e in entries if not e.is_dir]
        except Exception:
            return []
