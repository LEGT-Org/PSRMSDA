from dataclasses import dataclass
from datetime import datetime

from app.shared.config import settings
from app.shared.exception import (
    InvalidRefreshToken,
    ExpiredRefreshToken
)

from app.modules.auth.schema import StoredToken

@dataclass(frozen=True)
class StoredToken:

    value: StoredToken
    now: datetime


    def __post_init__(self):

        if self.value is None:
            raise InvalidRefreshToken()

        if self.value.revoked_at is not None:
            raise InvalidRefreshToken()

        if self.value.expires_at <= now:
            raise ExpiredRefreshToken()