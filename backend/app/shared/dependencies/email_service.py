from app.shared.email import SMTPEmailService, JinjaEmailRendered


def get_email_service() -> SMTPEmailService:
    return SMTPEmailService()


def get_email_renderer() -> JinjaEmailRendered:

    template_directory = (
        Path(__file__).resolve().parents[1]
        / "email"
        / "template"
    )

    return JinjaEmailRendered(str(template_directory))