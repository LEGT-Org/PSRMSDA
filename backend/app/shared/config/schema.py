from pydantic import BaseModel


class DomainSettings(BaseModel):

    allowed: set[str]

class FrontendSettings(BaseModel):

    url: str

class DatabaseSettings(BaseModel):

    driver: str
    host: str
    port: int
    username: str
    password: str
    name: str

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class EmailServiceSettings(BaseModel):

    host: str
    port: int
    username: str
    password: str
    sender: str
    use_tls: bool


class LLMServiceSettings(BaseModel):

    api_key: str
    model: str
    timeout: float


class AuthSettings(BaseModel):

    jwt_secret_key: str
    algorithm: str
    password_setup_token_expire_hours: int
    password_reset_token_expire_hours: int
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    registration_token_bytes:int
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