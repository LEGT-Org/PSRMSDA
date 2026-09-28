from pydantic_settings import BaseSettings, SettingsConfigDict

from app.shared.config.schema import (
    EmailServiceSettings,
    DatabaseSettings,
    FrontendSettings,
    CookieSettings,
    DomainSettings,
    AuthSettings, 
    CORSSettings
)


class Settings(BaseSettings):

    domain: DomainSettings
    frontend: FrontendSettings
    database: DatabaseSettings
    email: EmailServiceSettings
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