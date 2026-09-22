import hashlib
import secrets

from app.shared.config import settings


def generate_refresh_token() -> str:

    return secrets.token_urlsafe(settings.refresh_token_bytes)


def hash_refresh_token(token: str) -> str:

    return hashlib.sha256(token.encode()).hexdigest()