from pathlib import Path

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    login_username: str
    login_password: str
    logs_directory: DirectoryPath = Path("./logs")
    headless_mode: bool = True

    @classmethod
    def create_logs_directory(cls):
        # Get the current working directory
        current_directory = Path.cwd()

        # Create the logs directory (if not exists)
        logs_directory_path = current_directory / cls.logs_directory
        logs_directory_path.mkdir(parents=True, exist_ok=True)

        return logs_directory_path
