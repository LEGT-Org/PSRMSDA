import re

from dataclasses import dataclass

from app.shared.config import settings
from app.shared.exception import InvalidCredentialsError


email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$")


@dataclass(frozen=True)
class Email:

    value: str


    def __post_init__(self):

        match = email_regex.match(self.value)

        if not match:
            raise InvalidCredentialsError()

        domain = self.value.split("@")[-1].lower()

        if domain not in settings.allowed_domains:
            raise InvalidCredentialsError()