import pytest

from app.modules.auth.security.password import hash_password
from app.shared.config import settings


"""  

    Security Fixtures

"""

@pytest.fixture
def password():

    print("Creating password")
    return "secret123"


@pytest.fixture
def password_hash(password):

    print("Hashing password")
    return hash_password(password)


@pytest.fixture
def algorithms():

    print("Calling the algorithm from the .env file")
    return settings.algorithm


@pytest.fixture
def expected_duration_seconds():

    print("Setting the expected durations seconds")
    return settings.access_token_expire_minutes * 60