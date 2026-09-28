from datetime import datetime
from pydantic import (
    BaseModel, 
    EmailStr,
    SecretStr,
    ConfigDict,
    Field
)


class LoginRequest(BaseModel):

    email: str
    password: SecretStr


class TokenResponse(BaseModel):

    access_token: str
    token_type: str


class StoredToken(BaseModel):

    id: int
    user_id: int
    token_hash: str
    expires_at: datetime
    revoked_at: datetime
    created_at: datetime


class AuthResponse(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)