from pydantic import EmailStr

from app.modules.auth.schema import SetPasswordRequest
from app.modules.auth.interface import UserInterface

from app.shared.value_object.password import Password as PasswordValidation
from app.shared.security.password import hash_password, verify_password
from app.shared.value_object.user import Email as EmailValidation
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

    
    def auth_set_password(self, password_request: SetPasswordRequest):

        new_password = PasswordValidation(
            password=password_request.password, 
            confirm_password=password_request.confirm_password
        )

        password = hash_password(new_password.validated_password)

        self.interface.set_user_new_password(
            token_hash=password_request.token,
            new_password=password
        )

    
    def auth_reset_password(self, email: EmailStr):
        
        self.interface.password_reset(email=email)
