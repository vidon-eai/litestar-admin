from pathlib import Path
from advanced_alchemy.config import EngineConfig
from click import echo
from litestar.plugins.sqlalchemy import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin

from app.config.setting import settings
from app.core.base_model import Base
from app.modules.system.user.model import User


session_config = AsyncSessionConfig(expire_on_commit=False)
db_config = SQLAlchemyAsyncConfig(
    connection_string=settings.database_url,
    metadata=Base.metadata,
    before_send_handler="autocommit",
    session_config=session_config,
    engine_config=EngineConfig(
        echo=settings.database_echo
    )
)

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=db_config)
