from litestar import Litestar
from app.cli.commands import cli
from app.server.core import ApplicationCore


def create_app() -> Litestar:
    return Litestar(
        plugins=[ApplicationCore()],
    )


if __name__ == "__main__":
    cli()
