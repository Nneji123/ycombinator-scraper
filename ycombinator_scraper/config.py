from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    login_username: str
    login_password: str
    logs_directory: Path = Path("./logs")
    headless_mode: bool = True
