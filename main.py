from litestar import Litestar
from app.cli.commands import cli


def create_app() -> Litestar:
    from app.server.core import ApplicationCore    
    return Litestar(
        plugins=[ApplicationCore()],
    )


if __name__ == "__main__":
    cli()
