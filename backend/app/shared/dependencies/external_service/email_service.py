from pathlib import Path

from app.shared.infrastructure.email import SMTPEmailService, JinjaEmailRendered


def get_email_service() -> SMTPEmailService:
    return SMTPEmailService()


def get_email_renderer() -> JinjaEmailRendered:

    template_directory = (
        Path(__file__).resolve().parents[2]
        / "infrastructure"
        / "email"
        / "template"
    )

    return JinjaEmailRendered(str(template_directory))