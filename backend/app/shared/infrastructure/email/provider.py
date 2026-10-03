from typing import Protocol

from app.shared.infrastructure.email.message import EmailMessage

class EmailService(Protocol):

    def send(
        self, 
        email_service: EmailMessage
    ) -> None:
    
        pass