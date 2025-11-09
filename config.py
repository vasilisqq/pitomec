from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
import os
from pathlib import Path


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    BOT_LINK: SecretStr
    DB_URL: SecretStr
    REDIS_PASSWORD: SecretStr
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
