from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str
    jwt_secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    refresh_token_bytes: int
    allowed_domains: set[str]
    access_control_allowed_origin: set[str]
    allowed_credentials: bool
    allowed_methods: set[str]
    allowed_headers: set[str]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()