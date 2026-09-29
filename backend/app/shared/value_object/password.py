from dataclasses import dataclass

from app.shared.exception import (
    PasswordMustContainLowercaseError,
    PasswordMustContainUppercaseError,
    PasswordMustContainNumberError,
    PasswordDoesNotMatchError
)

@dataclass(frozen=True)
class Password:
    
    password: str
    confirm_password: str

    def __post_init__(self):

        self._validate_password(self.password)
        self._validate_password(self.confirm_password)
        self._validate_if_the_same(self.password, self.confirm_password)


    @staticmethod
    def _validate_password(password: str) -> None:

        if not any(char.isupper() for char in password):
            raise PasswordMustContainUppercaseError()

        if not any(char.islower() for char in password):
            raise PasswordMustContainLowercaseError()

        if not any(char.isdigit() for char in password):
            raise PasswordMustContainNumberError()


    @staticmethod
    def _validate_if_the_same(password: str, confirm_password: str) -> None:

        if password != confirm_password:
            raise PasswordDoesNotMatchError()


    @property
    def validated_password(self) -> str:

        return self.password    