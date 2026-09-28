import re

from dataclasses import dataclass

from app.shared.config import settings
from app.shared.exception import (
    NameOnlyContainAlphabeticCharacterError,
    NameMustBeTwoToFiftyCharacterError,
    InvalidCredentialsError,
    NoNameError
)


name_regex = re.compile(r"^[A-Za-z\s'-]+$")
email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$")


@dataclass(frozen=True)
class User:

    first_name: str
    last_name: str
    email: str


    def __post_init__(self):

        self._validate_name_field(self.first_name)
        self._validate_name_field(self.last_name)
        self._validate_email_field(self.email)

    
    @staticmethod
    def _validate_email_field(email: str) -> None:
        
        match = email_regex.match(email)

        if not match:
            raise InvalidCredentialsError()

        domain = email.split("@")[-1].lower()

        if domain not in settings.domain.allowed:
            raise InvalidCredentialsError()

    @staticmethod
    def _validate_name_field(name: str) -> None:

        cleaned_name = name.strip() if name else ""

        if not cleaned_name:
            raise NoNameError()

        if len(cleaned_name) < 2 or len(cleaned_name) > 50:
            raise NameMustBeTwoToFiftyCharacterError()

        if not name_regex.match(cleaned_name):
            raise NameOnlyContainAlphabeticCharacterError()


    @property
    def validated_first_name(self) -> str:

        return self.first_name

    @property
    def validated_last_name(self) -> str:

        return self.last_name

    @property
    def validated_email(self) -> str:

        return self.email


