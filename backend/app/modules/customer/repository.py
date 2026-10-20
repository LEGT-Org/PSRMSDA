from datetime import datetime
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.modules.customer.model import Customer
from app.modules.service_request.model import ServiceRequest

class CustomerRepository:

    def __init__(self, db: Session):

        self.db = db

    def create(
        self, 
        customer: Customer
    ) -> Customer:
        
        self.db.add(customer)
        return customer


    def get_all(
        self,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> tuple[list[Customer], int]:

        statement = select(Customer).where(
            Customer.email.isnot(None),
            Customer.deleted_at.is_(None)
        )

        if search and search.strip():
            search_value = f"%{search.strip()}%"

            statement = statement.where(
                or_(
                    Customer.first_name.ilike(search_value),
                    Customer.last_name.ilike(search_value),
                    Customer.email.ilike(search_value),
                    Customer.phone_number.ilike(search_value),
                )
            )

        count_statement = (
            select(func.count())
            .select_from(statement.subquery())
        )

        total = self.db.scalar(count_statement) or 0

        statement = (
            statement
            .order_by(Customer.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )

        customers = list(self.db.scalars(statement).all())

        return customers, total


    def get_by_id(
        self, 
        customer_id: int
    ) -> Customer | None:
        
        statement = select(Customer).where(
            Customer.id == customer_id,
            Customer.email.isnot(None),
            Customer.deleted_at.is_(None)
        )

        return self.db.scalar(statement)


    def has_service_requests(
        self, 
        customer_id: int
    ) -> bool:

        statement = (
            select(ServiceRequest.id)
            .where(
                ServiceRequest.customer_id == customer_id,
                Customer.deleted_at.isnot(None)
            )
            .limit(1)
        )

        return self.db.scalar(statement) is not None


    def get_customer_by_email(
        self, 
        email: str
    ) -> Customer | None:

        statement = select(Customer).where(Customer.email == email)
        return self.db.scalar(statement)


    def count_total_customers(
        self
    ) -> int:

        statement = (
            select(func.count())
            .select_from(Customer)
            .where(Customer.deleted_at.is_(None))
        )

        return self.db.scalar(statement) or 0


    def update(
        self,
        stored_customer: Customer,
        customer: dict,
        approve_by: int,
        now: datetime
    ) -> None:

        for field, value in customer.items():
            setattr(stored_customer, field, value)

        stored_customer.last_modified_by_id = approve_by
        stored_customer.updated_at = now


    def delete(
        self,
        stored_customer: Customer,
        approve_by: int,
        now: datetime
    ) -> None:

        stored_customer.last_modified_by_id = approve_by
        stored_customer.updated_at = now
        stored_customer.deleted_at = now
        stored_customer.email = None