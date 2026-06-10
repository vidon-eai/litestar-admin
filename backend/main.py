from litestar import Litestar
from app.cli.commands import cli
from app.core.storage import S3Storage
from app.utils.route_log import RouteLoggerPlugin
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: Litestar):
    from app.config.setting import app_setting
    from app.core.storage import OpenDALStorage

    if(app_setting.STORAGE_TYPE == "local"):
        app.state.storage = OpenDALStorage("fs")
    elif(app_setting.STORAGE_TYPE == "s3"):
        app.state.storage = S3Storage()
    else:
        app.state.storage = None

    # TODO: Add any startup logic here
    yield
    # TODO: Add any shutdown logic here



def create_app() -> Litestar:
    from app.server.core import ApplicationCore    
    return Litestar(
        plugins=[ApplicationCore(), RouteLoggerPlugin()],
        lifespan=[lifespan]
    )


if __name__ == "__main__":
    cli()
