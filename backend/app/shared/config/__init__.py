from pydantic_settings import BaseSettings, SettingsConfigDict

from app.shared.config.schema import (
    AuthSettings, 
    CORSSettings, 
    CookieSettings
)


class Settings(BaseSettings):

    database_url: str
    allowed_domains: set[str]
    
    auth: AuthSettings
    cors: CORSSettings
    cookie: CookieSettings
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )

settings = Settings()