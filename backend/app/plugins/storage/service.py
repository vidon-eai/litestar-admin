from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

from app.common.enums import StorageTypeEnum
from opendal import AsyncOperator

if TYPE_CHECKING:
    from .config import StorageConfig


class StorageService:
    """
    A service class for handling storage operations.
    """

    def __init__(self, config: "StorageConfig | None" = None) -> None:
        self.storage_type = config.storage_type.lower()

        if self.storage_type == StorageTypeEnum.S3:
            storage_config = {
                "endpoint": config.endpoint,
                "bucket": config.bucket,
                "access_key_id": config.access_key,
                "secret_access_key": config.secret_access_key,
                "region": config.region,
            }
        elif self.storage_type == StorageTypeEnum.LOCAL:
            root_path = config.root_path
            Path(root_path).mkdir(parents=True, exist_ok=True)
            storage_config = {
                "root": root_path,
            }
        else:
            raise ValueError(
                (f"不支援的儲存類型: {self.storage_type}，僅支援 'fs' 或 's3'")
            )
        print(config)
        self.op = AsyncOperator(scheme=config.storage_scheme, **storage_config)

    async def put(self, file_path: str, data: bytes) -> tuple[bool, str | None]:
        try:
            result = await self.op.write(file_path, data)
            return True, result
        except Exception as e:
            print(f"文件保存失败: {e}")
            return False, None

    async def get(self, file_path: str) -> Optional[bytes]:

        try:
            return await self.op.read(file_path)
        except Exception:
            return None

    async def delete(self, file_path: str) -> bool:
        print("Delete file:", file_path)
        try:
            await self.op.delete(file_path)
            return True
        except Exception as e:
            print(f"文件删除失败: {e}")
            return False

    async def list(self, prefix: str = "") -> List[str]:
        try:
            entries = await self.op.list(prefix)
            return [e.path for e in entries if not e.is_dir]
        except Exception:
            return []

    def exists(self, filename: str) -> bool:
        return self.op.exists(path=filename)
