from enum import StrEnum
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    EmailStr,
    SecretStr
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
    

class UserResponse(BaseModel):

    id: int
    first_name: str
    last_name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)