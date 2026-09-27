import smtplib
from email.message import EmailMessage

from app.shared.email.schema import EmailServiceSchema
from app.shared.config import settings


class SMTPEmailService:

    def send(
        self, 
        email_service: EmailServiceSchema
    ) -> None:

        message = EmailMessage()

        message["From"] = settings.email.sender
        message["To"] = email_service.to
        message["Subject"] = email_service.subject

        message.set_content(email_service.body)

        with smtplib.SMTP(
            settings.email.host,
            settings.email.port
        ) as smtp:

            if settings.email.use_tls:
                smtp.starttls()

            smtp.login(
                settings.email.username,
                settings.email.password
            )

            smtp.send_message(message)