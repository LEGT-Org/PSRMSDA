from pydantic import (
    BaseModel, 
    EmailStr,
    ConfigDict,
    Field
)


class UserCreate(BaseModel):

    first_name: str = Field(
        min_length=3,
        max_length=50
    )

    last_name: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )


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