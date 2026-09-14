from pydantic import BaseModel


class LoginRequest(BaseModel):

    email: str
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):

    refresh_token: str