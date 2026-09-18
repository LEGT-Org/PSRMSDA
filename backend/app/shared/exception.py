class EmailAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidRefreshToken(Exception):
    pass


class InvalidEmailAddressError(Exception):
    pass


class InvalidNameError(Exception):
    pass


class NameMustBeTwoToFiftyCharacterError(Exception):
    pass


class NameOnlyContainAlphabeticCharacter(Exception):
    pass


class ExpiredRefreshToken(Exception):
    pass