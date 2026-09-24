import re

from dataclasses import dataclass

from app.shared.exception import (
    InvalidNameError,
    NameMustBeTwoToFiftyCharacterError,
    NameOnlyContainAlphabeticCharacterError
)


name_regex = re.compile(r"^[A-Za-z\s'-]+$")


@dataclass(frozen=True)
class Name:

    value: str


    def __post_init__(self):

        cleaned_value = self.value.strip()

        if not cleaned_value:
            raise InvalidNameError()

        if len(cleaned_value) < 2 or len(cleaned_value) > 50:
            raise NameMustBeTwoToFiftyCharacterError()

        if not name_regex.match(cleaned_value):
            raise NameOnlyContainAlphabeticCharacterError()