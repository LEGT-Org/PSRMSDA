from pydantic import EmailStr

from app.modules.auth.interface import UserInterface

from app.shared.security.password import verify_password
from app.shared.exception import InvalidCredentialsError


class AuthService:

    def __init__(self, interface: UserInterface):

        self.interface = interface

    
    def authenticate_user(self, email: EmailStr, password: str):

        user = self.interface.get_user_by_email(email)

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        return user

    
    def auth_get_user_by_id(self, user_id: int):

        user = self.interface.get_user_by_id(user_id);

        return user

