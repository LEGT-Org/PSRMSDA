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