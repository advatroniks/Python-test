from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PASS: str
    DB_NAME: str
    DB_USER: str

    model_config = SettingsConfigDict(env_file=".env")


db_settings = DbSettings()
