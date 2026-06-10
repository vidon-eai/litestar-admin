from contextlib import asynccontextmanager
from litestar import Litestar

@asynccontextmanager
async def lifespan(app: Litestar):
    from app.config.setting import app_setting
    from app.core.storage import OpenDALStorage, S3Storage

    print("【Lifespan】应用启动，初始化存储驱动")
    match app_setting.STORAGE_TYPE:
        case "local":
            app.state.storage = OpenDALStorage(app_setting.STORAGE_LOCAL_PATH)
        case "s3":
            app.state.storage = S3Storage()
        case _:
            app.state.storage = None
            raise RuntimeError(f"不支持的存储类型: {app_setting.STORAGE_TYPE}")

    print(f"【Lifespan】存储驱动已挂载至 app.state，类型：{app_setting.STORAGE_TYPE}")
    yield