from litestar import Litestar
from app.cli.commands import cli
from app.utils.route_log import RouteLoggerPlugin

def create_app() -> Litestar:
    from app.server.core import ApplicationCore    
    return Litestar(
        plugins=[ApplicationCore(), RouteLoggerPlugin()],
    )


if __name__ == "__main__":
    cli()
