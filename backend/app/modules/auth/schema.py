from pydantic import (
    BaseModel, 
    EmailStr,
    ConfigDict
)


class RegisterRequest(BaseModel):
    
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):

    email: str
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):

    refresh_token: str


class UserResponse(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)