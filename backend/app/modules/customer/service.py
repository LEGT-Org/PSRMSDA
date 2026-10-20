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

        name = CustomerValidation(
            first_name=request.first_name,
            last_name=request.last_name
        )
        email = EmailValidation(request.email)
        phone_number = PhoneNumberValidation(request.phone_number)

        try:

            customer = Customer(
                first_name=name.validated_first_name,
                last_name=name.validated_last_name,
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

        customer = self.repository.get_by_id(customer_id)

        if customer is None:
            raise CustomerDoesNotExistError()

        updates = request.model_dump(exclude_unset=True)

        validated_updates = {}

        if "first_name" in updates or "last_name" in updates:

            name = CustomerValidation(
                first_name=updates.get("first_name") or customer.first_name,
                last_name=updates.get("last_name") or customer.last_name,
            )

            if updates.get("first_name") is not None:
                validated_updates["first_name"] = name.validated_first_name

            if updates.get("last_name") is not None:
                validated_updates["last_name"] = name.validated_last_name

        if "email" in updates and updates["email"] is not None:

            email = EmailValidation(email=updates["email"])
            validated_updates["email"] = email.validated_email

        if "phone_number" in updates and updates["phone_number"] is not None:

            phone_number = PhoneNumber(phone_number=updates["phone_number"])
            validated_updates["phone_number"] = phone_number.validated_phone_number

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
            raise CustomerUpdateFailedError() from error


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
            raise CustomerDeleteFailedError() from error
            

    def get_list_of_customers(
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

        pages = ceil(total / limit) if total else 0

        return CustomerPageListResponse(
            items=customers,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
        )


    def get_customer(
        self, 
        customer_id: int
    ) -> Customer:

        try:

            customer = self.repository.get_by_id(customer_id)

            if customer is None:
                raise CustomerDoesNotExistError()

            return customer

        except CustomerDoesNotExistError:

            raise

    
    def get_customer_counts(
        self
    ) -> int:

        return self.repository.count_total_customers()