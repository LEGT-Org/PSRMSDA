from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.shared.exception import CustomerDoesNotExistError
from app.shared.value_object.user import (
    PhoneNumber as PhoneNumberValidation,
    User as CustomerValidation,
    Email as EmailValidation
)

from app.modules.customer.schema import CustomerRequest, CustomerResponse
from app.modules.customer.repository import CustomerRepository
from app.modules.customer.model import Customer


class CustomerService:

    def __init__(
        self,
        repository: CustomerRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db


    def find_or_create_customer(
        self,
        customer_request: CustomerRequest
    ) -> CustomerResponse:

        customer_details = CustomerValidation(
            first_name=customer_request.first_name,
            last_name=customer_request.last_name
        )

        phone_number = PhoneNumberValidation(phone_number=customer_request.phone_number)
        email = EmailValidation(email=customer_request.email)

        stored_customer = self.repository.get_customer_by_email(email.validated_email)

        if stored_customer is not None:
            return stored_customer
        
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        customer = Customer(
            first_name=customer_details.validated_first_name,
            last_name=customer_details.validated_last_name,
            email=email.validated_email,
            phone_number=phone_number.validated_phone_number,
            created_at=now,
            updated_at=now,
            deleted_at=None
        )

        try:

            self.repository.create(customer)
            self.db.flush()

            return customer

        except Exception:

            self.db.rollback()
            raise CustomerDoesNotExistError()
            