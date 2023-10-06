from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PASS: str
    DB_NAME: str
    DB_USER: str

    model_config = SettingsConfigDict(env_file="/home/harold/Documents/TestTask_UnlimSoft/Python-test/.env")


db_settings = DbSettings()
