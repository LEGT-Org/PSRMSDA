from datetime import datetime

from pydantic import BaseModel, EmailStr


class CustomerRequest(BaseModel):

    first_name: str = Field(
        min_length=2,
        max_length=50
    )

    last_name: str = Field(
        min_length=2,
        max_length=50
    )

    email: EmailStr
    phone_number: str


class CustomerResponse(BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    created_at: datetime