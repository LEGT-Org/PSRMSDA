from typing import Protocol

from app.shared.email.schema import EmailServiceSchema

class EmailService(Protocol):

    def send(
        self, 
        email_service: EmailServiceSchema
    ) -> None:
    
        pass