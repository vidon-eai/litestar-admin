from datetime import datetime
from pathlib import Path
from advanced_alchemy.alembic.commands import AlembicCommands
from advanced_alchemy.utils.fixtures import open_fixture_async
from litestar.plugins.sqlalchemy import (
    SQLAlchemyInitPlugin,
)

from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy.exc import DBAPIError

from app.config.setting import app_setting

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=app_setting.DB_CONFIG)


async def create_tables() -> None:
    import app.db.models

    async with app_setting.DB_CONFIG.get_engine().begin() as conn:

        await conn.run_sync(UUIDv7AuditBase.metadata.create_all)


async def seed_database() -> None:
    fixtures_path = Path("app/db/fixtures")
    from app.core.logger import log
    from app.modules.system.user.service import UserService

    try:
        async with app_setting.DB_CONFIG.get_session() as db_session:
            user_service = UserService(session=db_session)

            user_data = await open_fixture_async(fixtures_path, "user")
            for user in user_data:
                if "dob" in user and isinstance(user["dob"], str):
                    # 將 "YYYY-MM-DD" 字串轉為 python 的 date 物件
                    user["dob"] = datetime.strptime(user["dob"], "%Y-%m-%d").date()
            await user_service.upsert_many(
                match_fields=["username"], data=user_data, auto_commit=True
            )

            log.info("✅ Seed data loaded successfully.")
    except DBAPIError as e:
        log.error(f"Data seed failed: {e}")


def upgrade_database(revision: str) -> None:

    alembic_cmds = AlembicCommands(sqlalchemy_config=app_setting.DB_CONFIG)
    alembic_cmds.upgrade(revision=revision)


def make_migrations(
    message: str, autogenerate: bool = True, head: str = "head"
) -> None:
    import app.db.models

    alembic_cmds = AlembicCommands(sqlalchemy_config=app_setting.DB_CONFIG)
    alembic_cmds.revision(message=message, autogenerate=autogenerate, head=head)
