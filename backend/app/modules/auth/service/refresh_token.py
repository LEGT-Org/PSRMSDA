from datetime import (
    datetime, 
    timedelta, 
    timezone
)

from fastapi import HTTPException, status

from app.modules.auth.model import RefreshToken
from app.modules.auth.repository import RefreshTokenRepository
from app.modules.auth.security.refresh_token import (
    generate_refresh_token, 
    hash_refresh_token
)

from app.shared.config import settings


class RefreshTokenService:
    
    def __init__(self, repository: RefreshTokenRepository):

        self.repository = repository

    
    def create_token(self, user_id: int) -> str:

        raw_token = generate_refresh_token()
        token_hash = hash_refresh_token(raw_token)
        now = datetime.now(timezone.utc)

        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=(now + timedelta(days=settings.refresh_token_expire_days)),
            created_at=now
        )

        self.repository.create(refresh_token)

        return raw_token


    def rotate_token(self, raw_token: str) -> tuple[int, str]:

        token_hash = hash_refresh_token(raw_token)
        stored_token = (self.repository.get_by_hash(token_hash))

        if stored_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        if stored_token.revoked_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        if stored_token.expires_at <= now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )

        user_id = stored_token.user_id
        
        self.repository.revoke(stored_token)

        new_token = self.create_token(user_id)

        return user_id, new_token