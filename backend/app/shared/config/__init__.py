from pydantic_settings import BaseSettings, SettingsConfigDict

from app.shared.config.schema import (
    AuthSettings, 
    CORSSettings, 
    CookieSettings,
    DatabaseSettings,
    DomainSettings
)


class Settings(BaseSettings):

    domain: DomainSettings
    database: DatabaseSettings
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