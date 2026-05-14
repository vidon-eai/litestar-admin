from pathlib import Path

# Project root path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Env file path
ENV_DIR = PROJECT_ROOT / "env"

# alembic config file path
ALEMBIC_CONFIG_DIR = PROJECT_ROOT / "app" / "db" / "migrations"
ALEMBIC_CONFIG_FILE = PROJECT_ROOT / "app" / "db" / "migrations" / "alembic.ini"
