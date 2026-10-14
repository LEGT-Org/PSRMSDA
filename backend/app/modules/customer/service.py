from math import ceil
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.shared.value_object.user import (
    PhoneNumber as PhoneNumberValidation,
    User as CustomerValidation,
    Email as EmailValidation
)

from app.shared.exception import (
    CustomerCreationFailedError, 
    CustomerDoesNotExistError,
    CustomerUpdateFailedError,
    CustomerDeleteFailedError,
    CustomerValidationError
)

from app.modules.customer.repository import CustomerRepository
from app.modules.customer.model import Customer
from app.modules.customer.schema import (
    CustomerPageListResponse,
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse,
    CustomerRequest
)

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

        except Exception as error:

            self.db.rollback()
            raise CustomerDoesNotExistError() from error


    def create_customer(
        self,
        actor_id: int,
        request: CustomerCreateRequest,
    ) -> Customer:

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        first_name = CustomerValidation(request.first_name)
        last_name = CustomerValidation(request.last_name)
        email = EmailValidation(request.email)
        phone_number = PhoneNumberValidation(request.phone_number)

        try:

            customer = Customer(
                first_name=first_name.validated_first_name,
                last_name=last_name.validated_last_name,
                email=email.validated_email,
                phone_number=phone_number.validated_phone_number,
                created_at=now,
                updated_at=now,
                deleted_at=None,
                last_modified_by_id=actor_id
            )

            self.repository.create(customer)
            self.db.commit()
            self.db.refresh(customer)

            return customer

        except Exception:

            self.db.rollback()
            raise CustomerCreationFailedError()


    def update_customer(
        self,
        actor_id:int,
        customer_id: int,
        request: CustomerUpdateRequest
    ) -> None:

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        customer = self.get_by_id(customer_id)

        if customer is None:
            raise CustomerDoesNotExistError()

        updates = request.model_dump(exclude_unset=True)

        validated_updates = {}

        for field, value in updates.items():

            if value is None:
                continue

            if field in ("first_name", "last_name"):
                validated_updates[field] = CustomerValidation(value).value

            elif field == "email":
                validated_updates[field] = EmailValidation(value).value

            elif field == "phone_number":
                validated_updates[field] = PhoneNumberValidation(value).value

        if not validated_updates:
            raise CustomerValidationError()

        try:

            self.repository.update(
                stored_customer=customer, 
                customer=validated_updates,
                approve_by=actor_id,
                now=now
            )

            self.db.commit()
            self.db.refresh(customer)

        except Exception as error:

            self.db.rollback()
            raise CustomerUpdateFailedError()


    def delete_customer(
        self,
        customer_id: int,
        actor_id: int
    ) -> None:

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        customer = self.repository.get_by_id(customer_id)

        if customer is None:
            raise CustomerDoesNotExistError()

        try:
            
            self.repository.delete(
                stored_customer=customer,
                approve_by=actor_id,
                now=now
            )

            self.db.commit()
            self.db.refresh(customer)

        except Exception as error:

            self.db.rollback()
            raise CustomerDeleteFailedError()
            

    def get_customers(
        self,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> CustomerPageListResponse:

        customers, total = self.repository.get_all(
            page=page,
            limit=limit,
            search=search,
        )

        return CustomerPageListResponse(
            items=customers,
            total=total,
            page=page,
            limit=limit,
            total_pages=ceil(total / limit) if total else 0,
        )


    def get_customer(
        self, 
        customer_id: int
    ) -> Customer:

        customer = self.repository.get_by_id(customer_id)

        if customer is None:
            raise CustomerDoesNotExistError()

        return customer
            