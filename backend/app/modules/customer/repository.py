from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.customer.model import Customer

class CustomerRepository:

    def __init__(self, db: Session):

        self.db = db

    def create(self, customer: Customer) -> Customer:
        
        self.db.add(customer)
        return customer


    def get_customer_by_email(self, email: str) -> Customer | None:

        statement = select(Customer).where(Customer.email == email)
        return self.db.scalar(statement)