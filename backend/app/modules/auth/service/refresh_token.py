from datetime import (
    datetime, 
    timedelta, 
    timezone
)

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.auth.model import RefreshToken
from app.modules.auth.repository import RefreshTokenRepository
from app.modules.auth.value_object.stored_token import StoredToken
from app.modules.auth.security.refresh_token import (
    generate_refresh_token, 
    hash_refresh_token
)

from app.shared.config import settings


class RefreshTokenService:
    
    def __init__(
        self,
        repository: RefreshTokenRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db

    
    def create_token(
        self, 
        user_id: int
    ) -> str:

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
        self.db.commit()
        self.db.refresh(refresh_token)

        return raw_token


    def rotate_token(
        self, 
        raw_token: str
    ) -> tuple[int, str]:

        token_hash = hash_refresh_token(raw_token)
        stored_token = (self.repository.get_by_hash(token_hash))
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        StoredToken(value=stored_token, now=now)

        user_id = stored_token.user_id
        
        self.repository.revoke(stored_token)
        self.db.commit()

        new_token = self.create_token(user_id)

        return user_id, new_token