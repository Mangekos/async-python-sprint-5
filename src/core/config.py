import os
from logging import config as logging_config

from pydantic import BaseSettings, Field, PostgresDsn

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

db_echo_mode = True

SECRET_KEY = "frgwergewrgerge"


class AppSettings(BaseSettings):
    app_title: str = Field(..., env="APP_TITLE")
    database_dsn: PostgresDsn = Field(..., env="DATABASE_DSN")
    project_name: str = Field(..., env="PROJECT_NAME")
    redis_host: str = Field("0.0.0.0", env="REDIS_HOST_NAME")
    redis_port: int = Field(6379, env="REDIS_PORT")
    elastic_host: str = Field("0.0.0.0", env="ELASTIC_HOST_NAME")
    elastic_port: int = Field(9200, env="ELASTIC_PORT")

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/../../.env"


app_settings = AppSettings()
