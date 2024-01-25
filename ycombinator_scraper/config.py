import platform
from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    login_username: str
    login_password: str
    logs_directory: str = Path("./logs")
    headless_mode: bool = True
    CHROME_BINARY: str = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    CHROMEDRIVER_BINARY: str = "chromedriver.exe"

    class Config:
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            # Override the default CHROMEDRIVER_BINARY based on the platform
            if platform.system() == "Windows":
                env_settings["CHROMEDRIVER_BINARY"] = "C:/chromedriver/chromedriver.exe"
            elif platform.system() == "Linux":
                env_settings["CHROMEDRIVER_BINARY"] = "/usr/local/bin/chromedriver"
            return init_settings, env_settings, file_secret_settings

        env_file = ".env"
