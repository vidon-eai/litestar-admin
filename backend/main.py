from litestar import Litestar
from app.cli.commands import cli
from app.utils.route_log import RouteLoggerPlugin
from app.utils.storage_lifespan import lifespan

def create_app() -> Litestar:
    from app.server.core import ApplicationCore    
    return Litestar(
        plugins=[ApplicationCore(), RouteLoggerPlugin()],
        lifespan=[lifespan]
    )


if __name__ == "__main__":
    cli()
