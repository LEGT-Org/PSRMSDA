class EmailAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidRefreshTokenError(Exception):
    pass


class InvalidEmailAddressError(Exception):
    pass


class InvalidNameError(Exception):
    pass


class NameMustBeTwoToFiftyCharacterError(Exception):
    pass


class NameOnlyContainAlphabeticCharacterError(Exception):
    pass


class ExpiredRefreshTokenError(Exception):
    pass