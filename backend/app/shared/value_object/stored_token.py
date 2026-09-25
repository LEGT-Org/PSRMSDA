from dataclasses import dataclass
from datetime import datetime

from app.shared.config import settings
from app.shared.exception import (
    InvalidRefreshTokenError,
    ExpiredRefreshTokenError
)

from app.modules.auth.schema import StoredToken

@dataclass(frozen=True)
class StoredToken:

    value: StoredToken
    now: datetime


    def __post_init__(self):

        if self.value is None:
            raise InvalidRefreshTokenError()

        if self.value.revoked_at is not None:
            raise InvalidRefreshTokenError()

        if self.value.expires_at <= self.now:
            raise ExpiredRefreshTokenError()