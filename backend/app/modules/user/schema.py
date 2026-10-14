from enum import StrEnum
from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    EmailStr
)


class UserRole(StrEnum):

    USER = "user"
    ADMIN = "admin"


class UserCreate(BaseModel):

    first_name: str = Field(
        min_length=2,
        max_length=50
    )

    last_name: str = Field(
        min_length=2,
        max_length=50
    )

    email: EmailStr


class RegistrationStoredUser(BaseModel):

    password_hash: str
    token_expire: datetime
    token_hash: str
    email_verified: bool


class UserPageResponse(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    role: str
    is_active: bool
    email_verified: bool
    created_at: datetime


class UserPageListResponse(BaseModel):

    items: list[UserPageResponse]
    page: int
    limit: int
    total: int
    pages: int
    

class UserResponse(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)