import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from app.shared.email.message import EmailMessage
from app.shared.config import settings
from app.shared.exception import (
    EmailServiceAuthenticationError,
    EmailServiceUnavailableError,
    EmailServiceFailedError
)

class SMTPEmailService:

    def send(self, message: EmailMessage) -> None:

        # 1. Create top-level container as 'related' for inline assets

        smtp_message = MIMEMultipart("related")
        smtp_message["From"] = settings.email.sender
        smtp_message["To"] = message.to
        smtp_message["Subject"] = message.subject

        # 2. Create an inner alternative container for Text + HTML

        msg_alternative = MIMEMultipart("alternative")
        smtp_message.attach(msg_alternative)

        # Attach plain text fallback

        msg_alternative.attach(MIMEText(message.body, "plain"))

        if message.html is not None:

            # Attach HTML part

            msg_alternative.attach(MIMEText(message.html, "html"))

            # 3. Read image

            logo_path = (
                Path(__file__).resolve().parent
                / "template"
                / "LEGT-Logo.png"
            )

            with logo_path.open("rb") as file:
                mime_image = MIMEImage(file.read(), _subtype="png")

            # CRITICAL: add_header on MIMEImage REQUIRES explicit angle brackets <>

            mime_image.add_header("Content-ID", "company-logo")
            mime_image.add_header("Content-Disposition", "inline", filename="LEGT-Logo.png")

            # Attach image directly to top-level related container

            smtp_message.attach(mime_image)

        # 4. Send
        
        try:

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

                smtp.sendmail(
                    settings.email.sender,
                    message.to,
                    smtp_message.as_string()
                )

        except smtplib.SMTPAuthenticationError as exc:
            raise EmailAuthenticationError() from exc

        except smtplib.SMTPConnectError as exc:
            raise EmailServiceUnavailableError() from exc

        except smtplib.SMTPException as exc:
            raise EmailServiceFailedError() from exc