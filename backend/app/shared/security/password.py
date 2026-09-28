import hashlib
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from app.shared.config import settings

password_hasher = PasswordHasher()


# Registration Password Hasher and Verificator

def hash_password(password: str) -> str:

    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:

    try:

        return password_hasher.verify(password_hash, password)

    except VerificationError:

        return False


# Registration Token For Verification

def generate_registration_token() -> str:

    return secrets.token_urlsafe(settings.auth.registration_token_bytes)


def hash_registration_token(token: str) -> str:

    return hashlib.sha256(token.encode()).hexdigest()