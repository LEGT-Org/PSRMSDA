from datetime import datetime

from pydantic import (
    ConfigDict, 
    BaseModel,
    EmailStr, 
    Field
)


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


class CustomerCreateRequest(BaseModel):

    first_name: str = Field(
        min_length=1, 
        max_length=100
    )

    last_name: str = Field(
        min_length=1, 
        max_length=100
    )

    email: str = Field(
        min_length=1, 
        max_length=255
    )

    phone_number: str = Field(
        min_length=1, 
        max_length=30
    )


class CustomerUpdateRequest(BaseModel):

    first_name: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=100
    )

    last_name: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=100
    )

    email: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=255
    )

    phone: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=30
    )


class CustomerUpdateResponse(BaseModel):

    id: int
    message: str


class CustomerResponse(BaseModel):
    
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerPageListResponse(BaseModel):

    items: list[CustomerResponse]
    total: int
    page: int
    limit: int
    pages: int