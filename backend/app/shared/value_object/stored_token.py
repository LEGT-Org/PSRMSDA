from typing import Any
from dataclasses import dataclass
from datetime import datetime

from app.shared.config import settings
from app.shared.exception import (
    InvalidRefreshTokenError,
    ExpiredRefreshTokenError
)

from app.modules.auth.schema import StoredTokenRequest

@dataclass(frozen=True)
class StoredRefreshToken:

    value: StoredTokenRequest
    now: datetime


    def __post_init__(self):

        self._validate_stored_token(self.value, self.now)

    
    @staticmethod
    def _validate_stored_token(stored_token: StoredTokenRequest, now: datetime) -> None:

        if stored_token is None:
            raise InvalidRefreshTokenError()

        if stored_token.revoked_at is not None:
            raise InvalidRefreshTokenError()

        if stored_token.expires_at <= now:
            raise ExpiredRefreshTokenError()


    @property
    def validated(self) -> dict[str, Any]:

        return self.value.model_dump()

    @property
    def user_id(self) -> int:
        
        return self.value.user_id