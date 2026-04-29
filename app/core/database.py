from pathlib import Path
from advanced_alchemy.config import EngineConfig
from advanced_alchemy.utils.fixtures import open_fixture_async
from click import echo
from litestar.plugins.sqlalchemy import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin

from app.config.setting import settings
from app.core.base_model import Base
from app.modules.system.user.model import User
from app.modules.system.user.service import UserRepo, UserService


db_config = SQLAlchemyAsyncConfig(
    connection_string=settings.database_url,
    before_send_handler="autocommit",
    session_config=AsyncSessionConfig(expire_on_commit=False),
    engine_config=EngineConfig(
        echo=settings.database_echo
    )
)

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=db_config)


async def create_tables() -> None:
    async with db_config.get_engine().begin() as conn:
       await conn.run_sync(Base.metadata.create_all)


async def seed_database() -> None:
    fixtures_path = Path("app/db/fixtures")
    from app.core.logger import log
    async with db_config.get_session() as db_session:
        user_service = UserService(session=db_session)
        
        user_data = await open_fixture_async(fixtures_path, "user")
        
        await user_service.upsert_many(
            match_fields=["username"],
            data=user_data,
            auto_commit=True
        )

        log.info("✅ Seed data loaded successfully.")