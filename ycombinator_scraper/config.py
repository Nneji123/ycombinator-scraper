from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import platform
# from typing import Dict


def get_chromedriver_binary() -> str:
    platform_name = platform.system().lower()
    if platform_name == "windows":
        return "C:/chromedriver/chromedriver.exe"
    elif platform_name == "linux":
        return "/usr/local/bin/chromedriver"
    else:
        return "chromedriver.exe"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    login_username: str
    login_password: str
    logs_directory: Path = Path("./logs")
    headless_mode: bool = True
    chromedriver_binary: str = Field(
        default=get_chromedriver_binary,
        env="CHROMEDRIVER_BINARY",
    )
