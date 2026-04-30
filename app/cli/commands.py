import os
from typing import Any
import anyio
import click
from app.core.database import create_tables, seed_database


@click.group(name="app", invoke_without_command=False, help="Application commands")
@click.pass_context
def app_cli(_: dict[str, Any]) -> None:
    """Application related commands."""


@app_cli.command(name="db")
def init_db() -> None:
    """Create database tables."""
    anyio.run(create_tables)
    click.echo("Database tables initialized.")


@app_cli.command(name="seed")
def init_data() -> None:
    """Load fixture data into database."""
    anyio.run(seed_database)
    click.echo("Database seed completed.")


@app_cli.command(name="start")
@click.option(
    "--env",
    help="服務器環境",
    type=click.Choice(["dev", "prod"]),
    default="dev",
    show_default=True,
    required=False,
)
@click.option(
    "--port", help="服務器端口", show_default=True, required=False, type=click.INT
)
def start_app(env: str, port: int | None) -> None:
    """启动生产或开发服务器"""
    os.environ["ENVIRONMENT"] = env

    import uvicorn
    from app.core.logger import setup_logging

    from app.config.setting import get_settings

    settings = get_settings()
    get_settings.cache_clear()
    setup_logging()
    uvicorn.run(
        "main:create_app",
        host=settings.server_host,
        port=port or settings.server_port,
        reload=settings.debug,
        factory=True,
        log_config=None,
    )


cli = app_cli
