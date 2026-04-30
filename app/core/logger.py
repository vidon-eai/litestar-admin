import atexit
import logging
from pathlib import Path
import sys

from loguru import logger
from typing_extensions import override

from app.config.setting import settings

# 全局变量记录日志处理器ID
_logger_handlers = []


class InterceptHandler(logging.Handler):
    """
    日誌攔截處理器：將所有 Python 標準日誌重定向到 Loguru
    """

    @override
    def emit(self, record: logging.LogRecord) -> None:
        # 嘗試獲取日誌級別名稱
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 獲取調用幀信息，確保 Loguru 顯示正確的原始代碼位置
        frame, depth = sys._getframe(), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # 使用 Loguru 記錄日誌，這會套用你定義的 log_format
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def cleanup_logging() -> None:
    """清理日誌資源[cite: 1]"""
    global _logger_handlers
    for handler_id in _logger_handlers:
        try:
            logger.remove(handler_id)
        except Exception as e:
            logger.opt(depth=1).warning(f"移除日誌處理器 {handler_id} 時出錯: {e}")
    _logger_handlers.clear()


def setup_logging() -> None:
    """
    配置日誌系統，實現 SQL 格式統一[cite: 1]
    """
    global _logger_handlers

    # 1. 配置 Loguru 基礎設定與格式[cite: 1]
    logger.configure(extra={"app_name": "Liststar Admin"})
    logger.remove()

    # 定義統一的格式[cite: 1]
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 添加輸出目標[cite: 1]
    _logger_handlers.append(
        logger.add(sys.stdout, format=log_format, level=settings.logger_level)
    )

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # 文件輸出[cite: 1]
    _logger_handlers.append(
        logger.add(
            str(log_dir / "info.log"),
            format=log_format,
            level="INFO",
            rotation="00:00",
            retention=30,
            compression="gz",
            encoding="utf-8",
        )
    )

    # 2. 攔截標準庫 logging 的 Root Logger[cite: 1]
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # 3. 專門針對 SQLAlchemy 進行格式統一化
    # 這些是 SQLAlchemy 常用的日誌名稱
    sql_loggers = [
        "sqlalchemy.engine",  # 顯示 SQL 語句
        "sqlalchemy.pool",  # 顯示連線池資訊
        "sqlalchemy.dialects",
        "sqlalchemy.orm",
    ]

    for name in sql_loggers:
        specific_logger = logging.getLogger(name)
        # 清除現有的 handler 防止重複輸出
        specific_logger.handlers = [InterceptHandler()]
        # 禁用傳播，確保日誌直接交給 InterceptHandler 處理，不再流向 Root Logger[cite: 1]
        specific_logger.propagate = False
        # 強制設定等級，確保能捕獲到日誌
        specific_logger.setLevel(settings.logger_level)

    # 4. 處理其餘第三方庫[cite: 1]
    for logger_name in logging.root.manager.loggerDict:
        if logger_name not in sql_loggers:
            _logger = logging.getLogger(logger_name)
            _logger.handlers = [InterceptHandler()]
            _logger.propagate = False

    atexit.register(cleanup_logging)


log = logger
