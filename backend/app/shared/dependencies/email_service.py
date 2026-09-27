from app.shared.email.smtp import SMTPEmailService


def get_email_service() -> SMTPEmailService:
    return SMTPEmailService()