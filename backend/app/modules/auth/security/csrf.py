import secrets

from typing import Annotated
from fastapi import (
    status,
    Cookie, 
    Header, 
    HTTPException
)

from app.shared.config import settings


def generate_csrf_token() -> str:

    return secrets.token_urlsafe(settings.csrf_token_bytes)


def validate_csrf(
    csrf_cookie: Annotated[
        str | None, 
        Cookie(alias="csrf_token")
    ] = None,
    csrf_headers: Annotated[
        str | None, 
        Header(alias="X-CSRF-Token")
    ] = None
):

    if (
        csrf_cookie is None
        or csrf_headers is None
        or not secrets.compare_digest(csrf_cookie, csrf_headers)
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid CSRF Token"
        )