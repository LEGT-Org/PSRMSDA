from app.modules.auth.schema import RegisterRequest
from app.modules.auth.security.password import hash_password


class AuthService:

    def __init__(self, interface: UserInterface):

        self.interface = user_interface

    
    def register(self, data: RegisterRequest):

        

        