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
    

class UserResponse(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)