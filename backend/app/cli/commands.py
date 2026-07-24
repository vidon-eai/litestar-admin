import os

import click
from app.cli.db import db_group
from app.cli.gen import gen_group


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
    from app.config.setting import get_app_setting
    from app.core.logger import setup_logging

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


# 註冊子 group
app_cli.add_command(db_group)
app_cli.add_command(gen_group)

cli = app_cli
