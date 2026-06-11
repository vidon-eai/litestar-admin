from litestar import Litestar
from app.cli.commands import cli
from app.utils.route_log import RouteLoggerPlugin
from app.utils.storage.storage_lifespan import storage_lifespan

def create_app() -> Litestar:
    from app.server.core import ApplicationCore    
    return Litestar(
        plugins=[ApplicationCore(), RouteLoggerPlugin()],
        lifespan=[storage_lifespan]
    )


if __name__ == "__main__":
    cli()
