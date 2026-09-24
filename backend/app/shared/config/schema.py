from pydantic import BaseModel


class AuthSettings(BaseModel):

    jwt_secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    refresh_token_bytes: int
    csrf_token_bytes: int


class CORSSettings(BaseModel):

    access_control_allowed_origin: set[str]
    allowed_credentials: bool
    allowed_methods: set[str]
    allowed_headers: set[str]


class CookieSettings(BaseModel):

    allowed_refresh_httponly: bool
    allowed_csrf_httponly: bool
    allowed_secure: bool
    allowed_samesite: str