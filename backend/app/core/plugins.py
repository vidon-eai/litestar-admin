from litestar.plugins.sqlalchemy import SQLAlchemyInitPlugin
from app.config.setting import app_setting

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=app_setting.DB_CONFIG)
