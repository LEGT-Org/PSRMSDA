from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone

from app.modules.auth.model import RefreshToken
from app.shared.config import settings


class RefreshTokenRepository:

    def __init__(self, db: Session):

        self.db = db

    
    def create(self, refresh_token: RefreshToken) -> RefreshToken:

        self.db.add(refresh_token)
        return refresh_token

    
    def get_by_hash(self, token_hash: str) -> RefreshToken | None:

        statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        return self.db.scalar(statement)

    
    def rotate(
        self,
        stored_token: RefreshToken,
        new_token_hash: str,
        now: datetime
    ) -> None:

        stored_token.token_hash = new_token_hash
        stored_token.expires_at = (now + timedelta(days=settings.refresh_token_expire_days))
        stored_token.revoked_at = None
        stored_token.created_at = now


    def revoke(self, refresh_token: RefreshToken) -> None:

        refresh_token.revoked_at = (datetime.now(timezone.utc).replace(tzinfo=None))