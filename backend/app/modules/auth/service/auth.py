from pydantic import EmailStr

from app.modules.auth.schema import UserCreate
from app.modules.auth.interface import UserInterface
from app.modules.auth.security.password import hash_password, verify_password

from app.shared.exception import InvalidCredentialsError


class AuthService:

    def __init__(self, interface: UserInterface):

        self.interface = interface

    
    def register(self, data: UserCreate):

        password_hash = hash_password(data.password)

        return self.interface.create_user(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=password_hash
        )

    
    def authenticate_user(self, email: EmailStr, password: str):

        user = self.interface.get_user_by_email(email)

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        return user