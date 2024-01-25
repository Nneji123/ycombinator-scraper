from pydantic import BaseSettings, Field
from pathlib import Path


class Settings(BaseSettings):
    login_username: str
    login_password: str
    logs_directory: Path = Path("./logs")
    headless_mode: bool = True
    CHROMEDRIVER_BINARY: str = "chromedriver.exe"

    class Config:
        env_file = ".env"

    # Override the default CHROMEDRIVER_BINARY based on the platform
    CHROMEDRIVER_BINARY: str = Field(
        default="chromedriver.exe",
        env="CHROMEDRIVER_BINARY",
        if_platform={
            "windows": "C:/chromedriver/chromedriver.exe",
            "linux": "/usr/local/bin/chromedriver",
        },
    )
