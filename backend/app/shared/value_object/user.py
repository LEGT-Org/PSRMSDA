import re

from dataclasses import dataclass

from app.shared.config import settings
from app.shared.exception import (
    NameOnlyContainAlphabeticCharacterError,
    NameMustBeTwoToFiftyCharacterError,
    InvalidCredentialsError,
    InvalidPhoneNumberError,
    NoNameError
)


# Name Validation

name_regex = re.compile(r"^[A-Za-z\s'-]+$")

@dataclass(frozen=True)
class User:

    first_name: str
    last_name: str

    def __post_init__(self):

        self._validate_name_field(self.first_name)
        self._validate_name_field(self.last_name)

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


# Email Validation

email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$")

@dataclass(frozen=True)
class Email:

    email: str

    def __post_init__(self):

        self._validate_email_field(self.email)

    @staticmethod
    def _validate_email_field(email: str) -> None:
        
        match = email_regex.match(email)

        if not match:
            raise InvalidCredentialsError()

        domain = email.split("@")[-1].lower()

        if domain not in settings.domain.allowed:
            raise InvalidCredentialsError()

    @property
    def validated_email(self) -> str:

        return self.email


# Phone Number Validation

e164 = re.compile(r"^\+[1-9]\d{6,14}$")
digits_and_plus = re.compile(r"[^\d+]")

@dataclass(frozen=True)
class PhoneNumber:

    phone_number: str


    def __post_init__(self):

        normalized = self.normalize(self.phone_number)

        self._validate_phone_number(normalize)

        object.__setattr__(self, "phone_number", normalized)
        
    
    @staticmethod
    def normalize(raw: str) -> str:
        
        normalized = digits_and_plus._STRIP.sub("", raw)
        return "+" + normalized.lstrip("+")

    @staticmethod
    def _validate_phone_number(normalized: str) -> None:
        
        if not E164.match(normalized):
            raise InvalidPhoneNumberError()


    @property
    def validated_phone_number(self) -> str:
        return self.phone_number

        