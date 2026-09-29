from datetime import datetime
from pydantic import (
    BaseModel, 
    EmailStr,
    ConfigDict,
    Field
)


class LoginRequest(BaseModel):

    email: str
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str


class StoredTokenRequest(BaseModel):

    id: int
    user_id: int
    token_hash: str
    expires_at: datetime
    revoked_at: datetime
    created_at: datetime


class SetPasswordRequest(BaseModel):

    token: str

    password: str = Field(
        min_length=8,
        max_length=128
    )

    confirm_password: str = Field(
        min_length=8,
        max_length=128
    )



class AuthResponse(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)