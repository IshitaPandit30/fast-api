from pydantic_settings import BaseSettings, SettingsConfigDict

from functools import lru_cache

class AppConfig(BaseSettings):
    app_name:str="FASTAPI"
    app_env:str="development"
    database_url:str

    model_config=SettingsConfigDict(env_file=".env")


@lru_cache  #cache the result of this function so that it doesn't read the .env file multiple times
def getAppConfig():
    return AppConfig()