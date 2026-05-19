import os
import sys
from advanced_alchemy.alembic.commands import AlembicCommands
import anyio
import click

from app.config.setting import app_setting
from app.core.database import make_migrations, upgrade_database


@click.group(name="app", invoke_without_command=False, help="Application commands")
def app_cli() -> None:
    """Application related commands."""
    pass


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

    from app.config.setting import get_app_setting

    app_setting = get_app_setting()
    get_app_setting.cache_clear()
    setup_logging()
    uvicorn.run(
        "main:create_app",
        host=app_setting.SERVER_HOST,
        port=port or app_setting.SERVER_PORT,
        reload=app_setting.DEBUG,
        factory=True,
        log_config=None,
    )


@app_cli.group(name="db", help="數據相關操作")
def db_group() -> None:
    """數據庫命令行"""
    pass


@db_group.command(name="init", help="初始化數據庫")
@click.option(
    "--env",
    help="服務器環境",
    type=click.Choice(["dev", "prod"]),
    default="dev",
    show_default=True,
    required=False,
)
def init_db(env: str) -> None:
    """Create database tables."""
    try:
        os.environ["ENVIRONMENT"] = env

        from app.core.database import create_tables

        anyio.run(create_tables)
        click.echo("Database tables initialized.")
    except Exception as e:
        click.echo(f"Database tables initialization failed: {e}")
        sys.exit(1)


@db_group.command(name="seed")
@click.option(
    "--env",
    help="服務器環境",
    type=click.Choice(["dev", "prod"]),
    default="dev",
    show_default=True,
    required=False,
)
def init_data(env: str) -> None:
    """Load fixture data into database."""
    try:
        os.environ["ENVIRONMENT"] = env
        from app.core.database import seed_database

        anyio.run(seed_database)
        click.echo("Data seed completed.")
    except Exception as e:
        click.echo(f"Data seed failed: {e}")
        sys.exit(1)


@db_group.command(name="upgrade")
@click.option(
    "--env",
    help="服務器環境",
    type=click.Choice(["dev", "prod"]),
    default="dev",
    show_default=True,
    required=False,
)
@click.option(
    "--revision",
    help="應用最新的 Alembic 遷移",
    default="head",
    show_default=True,
    required=False,
)
def db_upgrade(env: str, revision: str) -> None:
    os.environ["ENVIRONMENT"] = env
    upgrade_database(revision=revision)
    click.echo("數據庫遷移成功")


@db_group.command(name="migrate")
@click.option(
    "--env",
    help="服務器環境",
    type=click.Choice(["dev", "prod"]),
    default="dev",
    show_default=True,
    required=False,
)
@click.option(
    "--message",
    help="腳本名稱",
    required=True,
)
@click.option(
    "--autogenerate",
    help="是否自動生成腳本",
    type=click.BOOL,
    default="True",
    show_default=True,
    required=False,
)
@click.option(
    "--head",
    help="The head revision to base the new revision on",
    show_default=True,
    required=False,
)
def db_revision(env: str, message: str, autogenerate: bool, head: str) -> None:
    os.environ["ENVIRONMENT"] = env
    make_migrations(message=message, autogenerate=autogenerate, head=head)
    click.echo(f"生成數據庫{message}遷移腳本")


cli = app_cli
