from typing import Protocol

from app.shared.email.message import EmailMessage

class EmailService(Protocol):

    def send(
        self, 
        email_service: EmailMessage
    ) -> None:
    
        pass