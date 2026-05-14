from pathlib import Path
from advanced_alchemy.alembic.commands import AlembicCommands
from advanced_alchemy.config import AlembicAsyncConfig, EngineConfig
from advanced_alchemy.utils.fixtures import open_fixture_async
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)

from app.config.path_config import ALEMBIC_CONFIG_DIR, ALEMBIC_CONFIG_FILE

# from app.db.models.models import Base
from advanced_alchemy.base import UUIDv7AuditBase

from app.config.setting import settings

# db_config = SQLAlchemyAsyncConfig(
#     connection_string=settings.database_url,
#     before_send_handler="autocommit",
#     session_config=AsyncSessionConfig(expire_on_commit=False),
#     engine_config=EngineConfig(echo=settings.database_echo),
#     alembic_config=AlembicAsyncConfig(
#         script_location=f"{ALEMBIC_CONFIG_DIR}",
#         script_config=f"{ALEMBIC_CONFIG_FILE}",
#     ),
# )

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=settings.db_config)


async def create_tables() -> None:
    import app.db.models

    async with settings.db_config.get_engine().begin() as conn:

        await conn.run_sync(UUIDv7AuditBase.metadata.create_all)


async def seed_database() -> None:
    fixtures_path = Path("app/db/fixtures")
    from app.core.logger import log
    from app.modules.system.user.service import UserService

    async with settings.db_config.get_session() as db_session:
        user_service = UserService(session=db_session)

        user_data = await open_fixture_async(fixtures_path, "user")

        await user_service.upsert_many(
            match_fields=["username"], data=user_data, auto_commit=True
        )

        log.info("✅ Seed data loaded successfully.")


def upgrade_database(revision: str) -> None:

    alembic_cmds = AlembicCommands(sqlalchemy_config=settings.db_config)
    alembic_cmds.upgrade(revision=revision)


def make_migrations(
    message: str, autogenerate: bool = True, head: str = "head"
) -> None:

    alembic_cmds = AlembicCommands(sqlalchemy_config=settings.db_config)
    alembic_cmds.revision(message=message, autogenerate=autogenerate, head=head)
