from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str
    csv_filename: str = "output.csv"
    login_username: str
    login_password: str
    CHROME_BINARY: str = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    class Config:
        env_file = ".env"
