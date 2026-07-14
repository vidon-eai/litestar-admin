from contextlib import asynccontextmanager
from litestar import Litestar
from app.config.setting import app_setting
from app.utils.storage.local_storage import LocalStorage
from app.core.logger import log


@asynccontextmanager
async def storage_lifespan(app: Litestar):
    match app_setting.STORAGE_TYPE:
        case "local":
            app.state.storage = LocalStorage(app_setting.STORAGE_LOCAL_PATH)
        case _:
            app.state.storage = None
            raise RuntimeError(f"不支持的存储类型: {app_setting.STORAGE_TYPE}")

    log.info(f"✅ 初始化儲存驅動成功：{app_setting.STORAGE_TYPE}")
    yield
