from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.session import get_db

from app.modules.customer.repository import CustomerRepository
from app.modules.customer.service import CustomerService


def get_customer_repository(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> CustomerRepository:

    return CustomerRepository(db)


def get_customer_service(
    repository: Annotated[
        CustomerService,
        Depends(get_customer_repository)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> CustomerService:

    return CustomerService(
        repository=repository,
        db=db
    )