from pydantic_settings import BaseSettings, Field, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    login_username: str
    login_password: str
    logs_directory: Path = Path("./logs")
    headless_mode: bool = True
    chromedriver_binary: str

    model_config = SettingsConfigDict(env_file=".env")
    
    #Override the default CHROMEDRIVER_BINARY based on the platform
    chromedriver_binary: str = Field(
        default="chromedriver.exe",
        env="CHROMEDRIVER_BINARY",
        if_platform={
            "windows": "C:/chromedriver/chromedriver.exe",
            "linux": "/usr/local/bin/chromedriver",
        },
    )
