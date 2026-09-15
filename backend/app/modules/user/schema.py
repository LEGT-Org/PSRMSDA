from enum import StrEnum
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