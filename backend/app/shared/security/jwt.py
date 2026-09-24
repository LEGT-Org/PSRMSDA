import jwt
from datetime import datetime, timedelta, timezone

from app.shared.config import settings


def create_access_token(user_id: int, role: str) -> str:

    now = datetime.now(timezone.utc)

    expires_at = (
        datetime.now(timezone.utc) + timedelta(minutes=settings.auth.access_token_expire_minutes)
    )
    
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": expires_at
    }

    return jwt.encode(
        payload, 
        settings.auth.jwt_secret_key, 
        algorithm=settings.auth.algorithm
    )


def decode_access_token(token: str) -> dict:

    return jwt.decode(
        token,
        settings.auth.jwt_secret_key,
        algorithms=[settings.auth.algorithm]
    )